# for pyspark streaming
from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext

# for linear regression model
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import pandas as pd
import numpy as np

def parse_track_line(line):
    values = line.split(",")
    assert len(values) == 5
    for i in range(1,5):
        values[i] = float(values[i].strip().decode('utf-8', errors='ignore'))
    values[0].decode('ascii', errors='ignore')
    return values    

print("Creating/training Linear Regression model...")

# Load dataset for model training
data = pd.read_csv("spotify_model.csv")
labels = data['label']
data.drop(columns=['label'], axis=1, inplace=True)

# Create and train model
lr = LinearRegression(fit_intercept=True, normalize=True)
lr.fit(data.to_numpy(), labels)
mean_error = mean_absolute_error(labels, lr.predict(data.to_numpy()))

print("Linear regression model has been trained. (mean_error = %i)" % (mean_error))

# create spark configuration
conf = SparkConf()
conf.setAppName("SpotifyPopPrediction")
# create spark instance with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# creat the Streaming Context from the above spark context with window size 2 seconds
ssc = StreamingContext(sc, 2)
# setting a checkpoint to allow RDD recovery
ssc.checkpoint("checkpoint_SpotifyPop")
# read data from port 9009
tracks = ssc.socketTextStream("localhost",9009)

# Separate each track values
values = tracks.map(lambda track: parse_track_line(track))
# Create tuple (name, features)
tuples = values.map(lambda v: (v[0], np.asarray([v[1],v[2],v[3],v[4]], dtype=float)))
# Make prediction
prediction = tuples.map(lambda t: (t[0], lr.predict(t[1].reshape(1,-1))))
# Prediction tuples as nice strings and transform predicted value to a range using mean_error
predictionRange = prediction.map(lambda p: "%s\t > Predicted popularity: [%2f - %2f]" % (p[0], (p[1]-mean_error)[0], (p[1]+mean_error)[0]))
# Print predictions
predictionRange.pprint(100)

ssc.start()
ssc.awaitTermination()
