from pyspark.sql import SparkSession
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
#from delta.tables import *
#from delta import *


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .config("spark.app.name", "practice")\
        .config("spark.executor.instances", "1")\
        .config("spark.jars", "dags/app/postgresql-42.5.1.jar") \
        .config("spark.sql.shuffle.partitions", "1") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    flightSchemaDDL = """FL_DATE DATE, OP_CARRIER STRING, OP_CARRIER_FL_NUM INT, ORIGIN STRING, 
          ORIGIN_CITY_NAME STRING, DEST STRING, DEST_CITY_NAME STRING, CRS_DEP_TIME INT, DEP_TIME INT, 
          WHEELS_ON INT, TAXI_IN INT, CRS_ARR_TIME INT, ARR_TIME INT, CANCELLED INT, DISTANCE INT"""
    
    flightDF = spark.read \
        .format("csv") \
        .option("header", "true") \
        .schema(flightSchemaDDL) \
        .option("dateFormat", "d/M/y") \
        .load("dags/app/superset.csv")

    df = flightDF.withColumn("id", monotonically_increasing_id())

    DF = df[["id","fl_date", "op_carrier", "op_carrier_fl_num", "origin_city_name", "dest_city_name", "crs_dep_time", "dep_time", "wheels_on", "taxi_in", "crs_arr_time", "arr_time", "cancelled", "distance"]]
    DF.printSchema()

    DF.createOrReplaceTempView("temp")
    newDF = spark.sql("refresh temp")

    newDF.write\
    .format("jdbc") \
    .option("driver", "org.postgresql.Driver") \
    .option("url", "jdbc:postgresql://10.96.34.234:5432/airflow") \
    .option("user", "postgres") \
    .option("password", "airflow") \
    .option("dbtable", "dag_runs") \
    .mode("overwrite").save()
    










    #deltaTable = DeltaTable.forPath(spark, "dags/app/bronze/superset-csv")

    """if deltaTable:
        deltaTable.alias("oldData") \
                .merge(
                DF.alias("newData"),
                "oldData.id = newData.id") \
                .whenMatchedUpdate(set = { "id": col("newData.id") }) \
                .whenNotMatchedInsert(values = { "id": col("newData.id") }) \
                .execute()
    else:
        DF.write.format("delta").save("dags/app/bronze/superset-csv")"""
    

    

    

