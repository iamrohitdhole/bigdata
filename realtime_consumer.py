a) [5 points] Real-time Stream Consumer:Write a Python script using APIs to consume posts (data) from a specific keyword in real-time. Filter and pre-process the data (remove URLs, etc.)

import praw
import pandas as pd
import re

# Function to remove URLs from text
def remove_urls(text):
    return re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

# Reddit API authentication
reddit = praw.Reddit(client_id='V7KhOkbLo3cXf6ugdfizSQ',
                     client_secret='ImAdm5_25YvFKZOut6aSJz13rXopGg',
                     user_agent='Defiant_Train_2663')

# Define a function to fetch posts
def fetch_reddit_posts(subreddit, keyword, limit=10):
    submissions = reddit.subreddit(subreddit).search(keyword, limit=limit)
    filtered_posts = []
    for submission in submissions:
        title = remove_urls(submission.title)
        content = remove_urls(submission.selftext)
        filtered_posts.append((title, content))
    return filtered_posts

# Fetch posts for a specific subreddit and keyword
subreddit_name = 'dataengineering'  
keyword = 'big data'     
posts = fetch_reddit_posts(subreddit_name, keyword)

# Convert the posts to a DataFrame and display
df = pd.DataFrame(posts, columns=['Title', 'Content'])
print(df)
