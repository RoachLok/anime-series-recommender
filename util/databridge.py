from pyspark.sql import SparkSession, DataFrame

class Databridge():
    def __init__(self, data_location : str, name : str):
        self.spark_session = SparkSession.builder.master(data_location).appName(name).getOrCreate()
        self.dataframes = {}

    def get_spark_instance(self) -> SparkSession:
        return self.spark_session

    def add_dataframe(self, df : DataFrame, id : str):
        if id in self.dataframes:
            raise ValueError('id already in use.')

        self.dataframes[id] = df
    
    def get_dataframe(self, df_id : str) -> DataFrame:
        if df_id not in self.dataframes:
            return None
        
        return self.dataframes[df_id]

    def remove_dataframe(self, id : str) -> DataFrame:
        if id in self.dataframes:
            return self.dataframes.pop(id)
        else:
            return None

    def union_store(self, stored_id1 : str, stored_id2 :str) -> DataFrame:
        return self.dataframes[stored_id1].union(self.dataframes[stored_id2])

    def join_stored(self, stored_id1 : str, stored_id2 : str, on_join_tag : str) -> DataFrame:
        return self.dataframes[stored_id1].join(self.dataframes[stored_id2], on=on_join_tag)