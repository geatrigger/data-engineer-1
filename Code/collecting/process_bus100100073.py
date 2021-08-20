from pyspark.sql import SparkSession
from pyspark.sql.functions import explode

spark = SparkSession \
    .builder \
    .appName("bus100100073") \
    .getOrCreate()

busSchema = spark.read.format('json').load('/home/lab01/bus/20210813142502Bus100100073.json').schema
busDf = spark.readStream.schema(busSchema).json('/home/lab01/bus/*100100073.json')
df_bus = busDf.select(explode(busDf.ServiceResult.msgBody.itemList).alias("buses")).select('buses.*')
df_bus.coalesce(1).writeStream.format('json').option("checkpointLocation", "/home/lab01/bus100100073_check").option("path", "/home/lab01/bus100100073").trigger(processingTime='3600 seconds').start().awaitTermination()


