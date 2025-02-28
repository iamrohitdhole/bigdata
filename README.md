# Real-Time Sentiment Analysis using Reddit API

## Overview

This project implements a big data pipeline for real-time sentiment analysis of Reddit posts using the **Reddit API**, **Apache Kafka**, **Apache Spark**, and **Apache Hive**. The system reads posts from Reddit based on a specific keyword, performs sentiment analysis (positive, negative, neutral) using VADER sentiment analysis, and stores the results in a Hive table. The system uses Kafka for real-time data streaming and Spark Streaming for processing the data.

## Requirements

- **Python 3.x**
- **Kafka** (for real-time streaming)
- **Apache Spark** with PySpark
- **Apache Hive** (for storing data)
- **Reddit API credentials** (via PRAW)
- **VADER Sentiment Analysis** (for sentiment classification)
- **PySpark SQL** (for handling data with Spark)
- **Pandas, Kafka-python, Praw**, and other necessary Python libraries

### Installation Steps

1. **Install Required Tools:**
   - **Kafka and Zookeeper**: Follow the official [Kafka documentation](https://kafka.apache.org/quickstart) for installation and configuration on your local machine or cloud.
   - **Hive**: Follow the [Hive installation guide](https://cwiki.apache.org/confluence/display/Hive/GettingStarted) to install Hive and configure it to connect with Spark.
   - **Python Packages**:
     ```bash
     pip install pyspark[sql]
     pip install kafka-python
     pip install praw
     pip install vaderSentiment
     pip install pandas
     ```

2. **Set up Reddit API:**
   - Sign up for a Reddit Developer account and create an app [here](https://www.reddit.com/prefs/apps).
   - Generate your **API Key**, **API Secret**, and **User-Agent**.
   - Add your API credentials in the Python script.

3. **Set up Kafka:**
   - Make sure you have a running Kafka instance. If you are using a local instance, make sure to start both Kafka and Zookeeper.
   - Create a Kafka topic for Reddit posts:
     ```bash
     kafka-topics.sh --create --topic reddit_posts --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
     ```

4. **Set up Hive:**
   - Configure the Hive metastore and create the necessary database and table for storing sentiment data.
   - Example Hive table:
     ```sql
     CREATE TABLE sentiment_table (
         text STRING,
         sentiment STRING
     )
     STORED AS PARQUET;
     ```

## Application Overview

The pipeline performs the following tasks:

### 1. **Real-time Stream Consumer**:
   - Uses Reddit API to fetch posts based on a specific keyword.
   - Pre-processes the text to remove URLs and other unnecessary elements.

### 2. **Sentiment Analysis**:
   - Applies the **VADER Sentiment Analysis** model within Spark to classify each post as positive, negative, or neutral.
   - The sentiment of each post is determined based on the compound score provided by VADER.

### 3. **Real-time Data Storage**:
   - The sentiment-analyzed data is written to a Kafka topic and processed by Spark Streaming.
   - The data is then stored in a Hive table in **Parquet** format for further analysis.

### 4. **Visualization**:
   - Optionally, create visualizations in **Kibana** or **Grafana** to display the sentiment analysis results in real-time.

## How to Run the Application

### 1. **Start Kafka and Zookeeper**:
   - Start Zookeeper and Kafka if not already running:
     ```bash
     zookeeper-server-start.sh config/zookeeper.properties
     kafka-server-start.sh config/server.properties
     ```

### 2. **Start Hive Server**:
   - Start the HiveServer2 and make sure Hive is configured to connect with Spark:
     ```bash
     hive --service hiveserver2
     ```

### 3. **Run the Python Script**:
   - Replace the Reddit API credentials in the script.
   - Run the script to start consuming Reddit posts in real-time, performing sentiment analysis, and saving the results in Hive:
     ```bash
     python sentiment_analysis.py
     ```

### 4. **Verify the Data**:
   - You can verify the stored data by running a Hive query:
     ```sql
     SELECT * FROM sentiment_table;
     ```

## Challenges and Insights

### Challenges:
- **Kafka Setup**: Configuring Kafka and Zookeeper locally or on a cloud service required troubleshooting, especially with topic creation and ensuring proper connection settings.
- **Reddit API Limitations**: The Reddit API rate limits requests, so handling these limits efficiently was important in ensuring continuous data streaming.
- **Data Preprocessing**: Cleaning Reddit posts (removing URLs, special characters, etc.) posed a challenge when processing large amounts of unstructured data.

### Insights:
- **Kafka and Spark Integration**: The combination of Kafka for real-time streaming and Spark for data processing works efficiently in handling large datasets in real-time.
- **Hive for Data Storage**: Using Hive for storing Parquet files is beneficial as it provides schema management and query optimization for large-scale data.
- **Sentiment Analysis with VADER**: The VADER model provided a quick and effective way to perform sentiment analysis on textual data without requiring extensive training.

## Future Enhancements

- **Geographical Sentiment Analysis**: Incorporating geographical data (e.g., from users' locations) into the analysis to understand regional sentiment differences.
- **Advanced NLP Models**: Experiment with more advanced NLP models like BERT for improved sentiment accuracy.
- **Scaling with Cloud**: Move the setup to a cloud platform (e.g., AWS, GCP, Azure) to scale the pipeline for larger datasets.

## Conclusion

This project has provided hands-on experience in building a real-time big data pipeline using Kafka, Spark, and Hive. The integration of these tools for streaming data, processing, and storage in a distributed environment was both challenging and rewarding. The application successfully performs sentiment analysis on Reddit posts and provides a scalable solution for real-time data processing.

## Blog: https://medium.com/@rohitdhole18/building-a-real-time-big-data-pipeline-with-kafka-pyspark-and-reddit-api-372ef116e8c6 
