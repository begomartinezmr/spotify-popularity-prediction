from pyspark.sql.types import IntegerType,DoubleType,StringType
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StandardScaler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.functions import col, isnan,when,trim


#se supone que limpia de nulos, pero por lo visto no hay nulos
#lo que hay son caracteres especiales
def to_null(c):
    return when(~(col(c).isNull() | isnan(col(c)) | (trim(col(c)) == "")), col(c))


spark=SparkSession.builder.appName('Reg_log_Spotify_Model').getOrCreate()

#cargamos dataset
dataset=spark.read.csv("data.csv",header=True,inferSchema=True)

num_antes=dataset.count()



#limpiamos de nulos en el caso de haber
dataset=dataset.select([to_null(c).alias(c) for c in dataset.columns]).na.drop()

#dataset=dataset.na.drop().show(False)

##contamos numero de filas
num_des=dataset.count()

## en esta parte hacemos el cast de string a Double (sobre todo)
## ya que los datos cuando se cargan su tipo de convierte a string, no sé por qué
dataset = dataset.withColumn("explicit", dataset["explicit"].cast(IntegerType()))
dataset = dataset.withColumn("danceability", dataset["danceability"].cast(DoubleType()))

dataset = dataset.withColumn("duration_ms", dataset["duration_ms"].cast(IntegerType()))
dataset = dataset.withColumn("energy", dataset["energy"].cast(DoubleType()))



dataset.head()
##para mirar el esqueta del dataset(tipos)
dataset.printSchema()
##columnas que vamos a usar para entrenar el modelo, se puede aniadir o quitar
colums_name=['valence','year','acousticness','duration_ms']
##las trasformamos el tipo(ya que Spark Ml,funciona solo con este tipo  )
vec_assembler=VectorAssembler(inputCols=colums_name,outputCol='features')
##trandformamos nuestro data set al tipo deseado para Spark ML
data=vec_assembler.transform(dataset)
data.printSchema()
data.show(3)

#preparamos el dataset para entrenarlo(los modelos deSpark ML, solo necesitan el vector de columnas a usar y lo que 
#queremos predecir en este caso "explicit")
data_to_train=data.select('features','explicit')
data_to_train.printSchema()

##seleccionamos solo n columnas del dataset(por temas de limitacion de la MV)
data_to_train=data_to_train.limit(100)
print("+++++++++")
print(data_to_train.count())

##separamos conjutos de datos de entrenamiento y test
train, test=data_to_train.randomSplit([0.7,0.3])

#configuaramos el modelo de reg logistica
model=LogisticRegression(labelCol='explicit')
##lo entrenamos con el cjto de entrenamiento
model=model.fit(train)

summary=model.summary
##información acerca de los resultados entrenador
summary.predictions.describe().show()
##evaluamos el conjunto de test
predictions=model.evaluate(test)
##se muestran las predicciones
predictions.predictions.show()
##evalua la precision del modelo
evaluator=BinaryClassificationEvaluator(rawPredictionCol='prediction',labelCol='explicit')
## muestra el porcentaje de acierto
print(evaluator.evaluate(predictions.predictions))

print(num_antes)
print(num_des)


