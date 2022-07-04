from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType

rating_schema = StructType([ 
        StructField('user'          , IntegerType()), 
        StructField('item'          , IntegerType()),
        StructField('rating'        , IntegerType()) 
    ])

movies_schema = StructType([ 
        StructField('item'          , IntegerType()), 
        StructField('Name'          , StringType ()),
        StructField('Score'         , FloatType  ()),
        StructField('Genres'        , StringType ()),
        StructField('English name'  , StringType ()),
        StructField('Japanese name' , StringType ()),
        StructField('Type'          , StringType ()) 
    ])