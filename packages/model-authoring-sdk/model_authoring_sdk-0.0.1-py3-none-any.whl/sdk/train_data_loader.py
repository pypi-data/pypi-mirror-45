from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import LongType, DoubleType, IntegerType, StringType
from pyspark.sql import Row
from sdk.data_loader import DataLoader


class TrainDataLoader(DataLoader):

    def load(self, configProperties, spark):

        #spark.sparkContext._jsc.hadoopConfiguration().set(str(spark.sparkContext.getConf().get("CONF_blobStoreAccount_KEY")),str(spark.sparkContext.getConf().get("CONF_blobStoreAccount_VALUE")))
        #trainingDataLocation = str(configProperties.get("trainingDataLocation"))

        #trainingSchema = StructType([
        #    StructField("id", LongType()),
        #    StructField("user", StringType()),
        #    StructField("text", StringType()),
        #    StructField("label", DoubleType())
        #])

        #training = spark.read.schema(trainingSchema).format("csv").option("mode", "DROPMALFORMED").csv(trainingDataLocation)
        #return training

        #l = [('Ankit', 25), ('Jalfaizy', 22), ('saurabh', 20), ('Bala', 26)]
        #rdd = spark.parallelize(l)
        #people = rdd.map(lambda x: Row(name=x[0], age=int(x[1])))
        #peopleDataFrame = sqlContext.createDataFrame(people)
        #peopleDataFrame.show()

        training = spark.createDataFrame([
            (0, "a b c d e spark", 1.0),
            (1, "b d", 0.0),
            (2, "spark f g h", 1.0),
            (3, "hadoop mapreduce", 0.0)
        ], ["id", "text", "label"])
        return training