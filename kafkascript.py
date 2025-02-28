import praw
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from kafka import KafkaProducer
from kafka.errors import KafkaError
import time

# Reddit API authentication
reddit = praw.Reddit(client_id='V7KhOkbLo3cXf6ugdfizSQ',
                     client_secret='ImAdm5_25YvFKZOut6aSJz13rXopGg',
                     user_agent='Defiant_Train_2663')

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Function to fetch posts and analyze sentiment
def fetch_and_send_to_kafka(subreddit, keyword, limit=10):
    submissions = reddit.subreddit(subreddit).search(keyword, limit=limit)
    for submission in submissions:
        title = submission.title
        content = submission.selftext
        # Analyze sentiment
        sentiment = analyzer.polarity_scores(content)
        sentiment_label = 'neutral'
        if sentiment['compound'] >= 0.05:
            sentiment_label = 'positive'
        elif sentiment['compound'] <= -0.05:
            sentiment_label = 'negative'
        
        # Create message
        message = {
            'title': title,
            'content': content,
            'sentiment': sentiment_label
        }
        
        # Send message to Kafka topic
        try:
            future = producer.send('reddit_sentiment_topic', message)
            # Block until a single message is sent (optional)
            record_metadata = future.get(timeout=10)
            print(f"Sent message to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")
        except KafkaError as e:
            print(f"Failed to send message: {e}")

        # Optional: Sleep to avoid hitting Reddit API rate limits
        time.sleep(1)

# Fetch and send posts for a specific subreddit and keyword
subreddit_name = 'all'
keyword = 'big data'
fetch_and_send_to_kafka(subreddit_name, keyword)

# Flush and close the producer
producer.flush()
producer.close()
