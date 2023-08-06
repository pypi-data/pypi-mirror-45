from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.sql import SparkSession
from sdk.pipeline_factory import PipelineFactory

class TrainPipeline(PipelineFactory):

    def apply(self, configProperties):

        # Reading configs from config properties.
        maxIterVal = int(configProperties.get("maxIter"))
        regParamVal = float(configProperties.get("regParam"))
        #numFeaturesVal: Int  = configProperties.get("numFeatures").get.toInt

        # Configure an ML pipeline, which consists of three stages: tokenizer, hashingTF, and lr.
        #tokenizer = Tokenizer(inputCol="text", outputCol="words")
        #hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features")
        #lr = LogisticRegression(maxIter=maxIterVal, regParam=regParamVal)
        #pipeline = Pipeline(stages=[tokenizer, hashingTF, lr])

        #return pipeline

        tokenizer = Tokenizer(inputCol="text", outputCol="words")
        hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features")
        lr = LogisticRegression(maxIter=10, regParam=0.001)
        pipeline = Pipeline(stages=[tokenizer, hashingTF, lr])
        return pipeline

    def getParamMap(self, configProperties, sparkSession):
        return None
