from pyspark.sql import DataFrame
from pyspark.ml.recommendation import ALS
from pyspark.sql.types import Row
from pyspark.sql.functions import when

class Recommender:
    def __init__(self, maxIter=5):
        self.als = ALS(rank=10, seed=0)
        self.als.setMaxIter(maxIter)
        self.models = {}

    def trainModel(self, ratings_df : DataFrame, model_id : str):
        model = self.als.fit(ratings_df)
        model.setPredictionCol('predic')
        model.userFactors.orderBy("id").collect()

        self.models[model_id] = model
   
    def getUserPredictions(self, user_id : str, ratings_wtype : DataFrame, model_id : str) -> list[Row]:
        not_seen_by_user = ratings_wtype.withColumn('user', when(ratings_wtype['user'] != user_id, user_id).otherwise(-1)) \
                            .where('Type == "TV" or Type == "Movie"').dropDuplicates(['item']).where('user != -1')  # For now filtering TV and Movie only.
        # This is returning all predictions for the given user where Type is TV or Movie.
        # Returns them sorted by Type so that splitting is faster.
        return self.models[model_id].transform(not_seen_by_user['user','item', 'Type']).sort('Type', 'predic', ascending=False).collect()