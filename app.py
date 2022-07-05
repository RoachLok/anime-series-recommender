from bcrypt import re
from flask import Flask, render_template, request, redirect, session
from flask_caching import Cache
import schema.data_structs as schemas
from util.databridge import Databridge
from util.model import User
from transform.recommend import Recommender
from util.cataloguer import JikanRequest, YTRequest, Cataloguer
from random import randrange

data = Databridge(data_location='local[7]', name='Anime_recommender')

# Loading all ratings. Treating EP as a regular user for now.
data.add_dataframe(data.get_spark_instance().read.csv('data/rating_complete_small.csv', header=True, schema=schemas.rating_schema), 'ratings'   )
data.add_dataframe(data.get_spark_instance().read.csv('data/valoraciones_EP.csv'      , header=True, schema=schemas.rating_schema), 'EP_ratings')   
data.add_dataframe(data.union_store('ratings', 'EP_ratings'), 'all_ratings')

# Load items info
data.add_dataframe(data.get_spark_instance().read.csv('data/anime.csv', header=True, schema=schemas.movies_schema), 'items')
# Join items with ratings to filter by category.
data.add_dataframe(data.get_dataframe('all_ratings').join(data.get_dataframe('items')['item', 'Type'], on='item'), 'ratings_wtype')

config = {   
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "SECRET_KEY": "64283451_ 4v3ry s3cret K3y th15 is._2584569"
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

run_id = randrange(1000,9999)

users = {}
recommender = Recommender()

req_jikan = JikanRequest('http://AnimeRecommender-jikan_api:8000/v3')
req_ytube = YTRequest('bin/yt-dlp')
cataloguer = Cataloguer([req_jikan, req_ytube])

# Training the model, for now we only train based on 1 dataset. 
# Training only on ratings and user ids. Excluding other parameters such as "to watch".
recommender.trainModel(data.get_dataframe('all_ratings'), 'all_ratings_model')

@app.route('/')
def index():
    session['run_id'] = run_id
    return render_template('fake_login.html')

@app.route('/good_index')
def good_index():
    if 'run_id' not in session or 'user_id' not in session or session['run_id'] != run_id:
        return redirect('/', code=302)
    
    current_user = session['user_id']

    return render_template('good_index.html', movies=users[current_user].getRecommendedMovies(), series=users[current_user].getRecommendedSeries())

@app.route('/verifying', methods=['GET', 'POST'])
def verifying():    # Does not just verify the user, it also generates predictions for the selected user.
    if request.method == 'GET':
        return redirect('/')

    current_user = request.form.get('user-id', '666666')
    if not current_user.isdigit():
        current_user = 666666
    
    current_user = int(current_user)

    if current_user not in users:
        curr_user = User(current_user)
        user_predictions = recommender.getUserPredictions(current_user, data.get_dataframe('ratings_wtype'), 'all_ratings_model')
        curr_user.setRecommendations  ( [spark_row.asDict() for spark_row in user_predictions] )
        curr_user.setRecommendedMovies( cataloguer.catalogue_predictions(curr_user.getRecommendedMovies()) )
        curr_user.setRecommendedSeries( cataloguer.catalogue_predictions(curr_user.getRecommendedSeries()) )
        
        users[current_user] = curr_user

    session['user_id'] = current_user

    return redirect('/good_index', code=303)

@app.route('/home')
def home():
    if 'run_id' not in session or 'user_id' not in session or session['run_id'] != run_id:
        return redirect('/', code=302)
    
    current_user = session['user_id']

    return render_template('index.html', movies=users[current_user].getRecommendedMovies(), series=users[current_user].getRecommendedSeries())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
