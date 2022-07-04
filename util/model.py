from pyspark.sql.dataframe import DataFrame

class User:
    def __init__(self, id : str):
        self.id = id

        self.movie_recommendations = []  # '0':'No recommendations.'
        self.serie_recommendations = []  # '0':'No recommendations.'

    def getId(self) -> str:
        return self.id
    
    def setRecommendations(self, recs_wtype : list, split_movies_TV = True, n=11):
        # recs_wtype: Recommendations with type.
        # This code is not safe, but does the job for the test dataset. 
        # Takes a sorted by type list of recs and sets user recomended
        # series and movies if asked for. 
        self.setRecommendedSeries(recs_wtype[:n])
        if split_movies_TV:
            data_pivot = find_splitting_index(recs_wtype, 'Movie')
            self.setRecommendedMovies(recs_wtype[data_pivot:][:n])

    def setRecommendedSeries(self, series : list):
        self.serie_recommendations = series

    def setRecommendedMovies(self, series : list):
        self.movie_recommendations = series

    def getRecommendedMovies(self) -> list:
        return self.movie_recommendations
    
    def getRecommendedSeries(self) -> list:
        return self.serie_recommendations


def find_splitting_index(list : list, second_key) -> int:
    # binarysearch-likeish approach to make splitting
    # the recs list by type faster. Recs are sorted by type. 
    if list[len(list)//2]['Type'] == second_key:
        for i in range (2*len(list)//3, 0, -1):
            if list[i-1]['Type'] == "TV":
                return i
    elif list[3*len(list)//5]['Type'] == second_key:
        for i in range (2*len(list)//3, 0, -1):
            if list[i-1]['Type'] == "TV":
                return i
    elif list[4*len(list)//5]['Type'] == second_key:
        for i in range (3*len(list)//4, 0, -1):
            if list[i-1]['Type'] == "TV":
                return i
    else:
        for i in range (len(list)-1, 0, -1):
            if list[i-1]['Type'] == "TV":
                return i
    return -1
    
# No longer needed. Here just in case.
def join_movies(ratings : DataFrame, items : DataFrame) -> DataFrame:
    return ratings.join(items, ratings['item'] == items['id'])