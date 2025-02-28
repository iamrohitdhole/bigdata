from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

# Initialize SparkContext and StreamingContext
sc = SparkContext(appName="SentimentAnalysis")
ssc = StreamingContext(sc, 10)  # 10-second batch interval

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to analyze sentiment using VADER
def analyze_sentiment(text):
    sentiment_score = analyzer.polarity_scores(text)
    compound_score = sentiment_score['compound']

    if compound_score >= 0.05:
        return 'positive'
    elif compound_score <= -0.05:
        return 'negative'
    else:
        return 'neutral'

# Function to process incoming data and analyze sentiment
def process_rdd(rdd):
    # Parse the RDD to extract posts and analyze sentiment
    if not rdd.isEmpty():
        posts = rdd.map(lambda x: json.loads(x[1]))  # Assuming each Kafka message is in JSON format
        sentiments = posts.map(lambda post: analyze_sentiment(post['text']))  # Assuming each post has 'text' field
        sentiments.pprint()  # Print the sentiment for each post

# Kafka Stream Setup (Replace with actual Kafka parameters)
kafkaStream = KafkaUtils.createStream(ssc, 'localhost:2181', 'sentiment-group', {'reddit-posts': 1})

# Apply processing to the Kafka stream
kafkaStream.foreachRDD(process_rdd)

# Start the Spark Streaming Context
ssc.start()
ssc.awaitTermination()
