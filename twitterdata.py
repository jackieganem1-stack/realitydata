import tweepy
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import pandas as pd
import nltk
import json
import os

nltk.download('vader_lexicon')

# ✅ Your Twitter API v2 Bearer Token
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAACQY0wEAAAAASOhRrrcnq7fA8OpWiV%2FnxqoozZM%3Dc9hHvJ7nHsgecQE2Ra169VrQPV1JPi2NjnoOyA5GcBsglxe50N'
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Cache file path
CACHE_FILE = "tweets_cache.json"

# Fetch tweets from Twitter or cache
def get_tweets_v2(query, max_results=100):
    if os.path.exists(CACHE_FILE):
        print("📦 Using cached tweets from file.")
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)

    tweets_data = []
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=min(max_results, 100),
            tweet_fields=['text', 'lang', 'created_at']
        )
        if response.data:
            for tweet in response.data:
                if tweet.lang == "en":
                    tweets_data.append({
                        'text': tweet.text,
                        'created_at': tweet.created_at.isoformat()
                    })

            # Save to cache
            with open(CACHE_FILE, 'w') as f:
                json.dump(tweets_data, f)
            print("💾 Tweets saved to cache.")
    except tweepy.TooManyRequests:
        print("⏳ Rate limit hit. Try again later.")
    except Exception as e:
        print(f"Error fetching tweets: {e}")
    return tweets_data

# Sentiment analysis
def analyze_sentiment_over_time(tweets_data):
    analyzer = SentimentIntensityAnalyzer()
    results = []
    for item in tweets_data:
        score = analyzer.polarity_scores(item['text'])['compound']
        results.append({
            'time': pd.to_datetime(item['created_at']),
            'sentiment': score
        })
    df = pd.DataFrame(results)
    df.sort_values('time', inplace=True)
    return df

# Plot sentiment trend
def plot_sentiment_time_series(df):
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='time', y='sentiment', data=df, marker='o')
    plt.title('Sentiment Trend Over Time')
    plt.xlabel('Time')
    plt.ylabel('Compound Sentiment Score')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Main function
if __name__ == "__main__":
    celebrity = input("Enter the celebrity's name to analyze sentiment: ")
    tweets_data = get_tweets_v2(celebrity, max_results=100)
    if not tweets_data:
        print("No tweets available.")
        exit()

    df_sentiment = analyze_sentiment_over_time(tweets_data)

    print(f"\n🔍 Analyzed {len(df_sentiment)} tweets about {celebrity}")
    print(f"📊 Average Sentiment: {df_sentiment['sentiment'].mean():.2f}")

    plot_sentiment_time_series(df_sentiment)

