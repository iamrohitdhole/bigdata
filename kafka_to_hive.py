# Install necessary packages
!pip install pyspark vaderSentiment kafka-python

# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import pandas as pd

# Initialize SparkSession and StreamingContext
spark = SparkSession.builder \
    .appName("SentimentAnalysisWithKafka") \
    .enableHiveSupport() \
    .getOrCreate()

# Create StreamingContext for processing
ssc = StreamingContext(spark.sparkContext, 10)  # 10 seconds batch interval

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
    if not rdd.isEmpty():
        # Convert RDD to DataFrame
        df = rdd.toDF(["value"])
        
        # Parse JSON in the DataFrame
        posts = df.selectExpr("CAST(value AS STRING)").rdd.map(lambda row: json.loads(row[0]))
        
        # Create DataFrame from JSON
        posts_df = spark.read.json(posts)
        
        # Analyze sentiment
        sentiment_udf = spark.udf.register("analyze_sentiment", analyze_sentiment)
        posts_df = posts_df.withColumn("sentiment", sentiment_udf(posts_df["text"]))
        
        # Write to Kafka
        posts_df.write \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("topic", "sentiment-output") \
            .save()

        # Write to Hive in Parquet format
        posts_df.write \
            .mode("append") \
            .format("parquet") \
            .saveAsTable("sentiment_analysis_data")

# Kafka Stream Setup (Replace with actual Kafka parameters)
kafkaStream = KafkaUtils.createStream(ssc, 'localhost:2181', 'sentiment-group', {'input-topic': 1})

# Apply processing to the Kafka stream
kafkaStream.foreachRDD(process_rdd)

# Start the Spark Streaming Context
ssc.start()
ssc.awaitTermination()

# Assuming you have a CSV file to simulate the process
# Example of CSV file loading for sentiment analysis (use your own CSV file)
file_path = "/path/to/your/file.csv"

# Load CSV file into DataFrame
csv_data = pd.read_csv(file_path)

# Print first few rows of the CSV data
csv_data.head()

# Sentiment analysis for CSV data (using VADER)
csv_data['sentiment'] = csv_data['text'].apply(lambda x: analyze_sentiment(x))

# Convert analyzed data to a DataFrame for further processing
analyzed_data = spark.createDataFrame(csv_data)

# Write the analyzed data to Hive in Parquet format
analyzed_data.write \
    .mode("overwrite") \
    .format("parquet") \
    .saveAsTable("sentiment_analysis_data")
