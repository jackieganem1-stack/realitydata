import praw
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import math

# Optional: Categorize sentiment as Positive, Negative, or Neutral
def categorize_sentiment(compound_score):
    if not math.isnan(compound_score):
        if compound_score > 0.05:
            return "Positive"
        elif compound_score < 0.05:
            return "Negative"
        else:
            print("--------")
            print(compound_score)
            return "Neutral"


# Authenticate with Reddit API
reddit = praw.Reddit(
    client_id='7m09T71RyrT9PuWpfrXEjg',
    client_secret='FCMgp8KgX3MIdw4Cpw1wg3h9AQTy8g',
    user_agent='Unfair-Suggestion-19'
)

# Initialize VADER SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Function to perform sentiment analysis using VADER
def analyze_sentiment(text):
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']  # Compound score represents overall sentiment

# Define the celebrity name you're interested in
celebrity_name = 'Tom Sandoval'

# Define the time interval for sampling (e.g., '1D' for daily intervals)
time_interval = '22H'  # '1H' for hourly, '1D' for daily, etc.

# Search for posts/comments mentioning the celebrity name
subreddit = reddit.subreddit('all')  # Search across all subreddits

# Fetch posts or comments mentioning the celebrity
mentions = subreddit.search(celebrity_name, sort='new')  # Adjust the limit as needed

# List to store sentiment data
sentiment_data = []

# Loop through the search results (posts and comments)
for mention in mentions:
    # Get the timestamp of the post or comment
    post_timestamp = datetime.datetime.utcfromtimestamp(mention.created_utc)

    # Get the text of the post or comment
    mention_text = mention.title + " " + mention.selftext if hasattr(mention, 'selftext') else mention.body

    # Perform sentiment analysis on the mention text
    sentiment_score = analyze_sentiment(mention_text)

    # Only keep valid sentiment scores (numeric values)
    if isinstance(sentiment_score, (int, float)):
        sentiment_data.append({
            'timestamp': post_timestamp,
            'sentiment_score': sentiment_score,
            'mention_text': mention_text
        })
    else:
        print(f"Non-numeric sentiment score encountered for post: {mention.title}")

# Convert the sentiment data to a DataFrame
df = pd.DataFrame(sentiment_data)

# Ensure that sentiment_score is numeric and handle errors by converting invalid values to NaN
df['sentiment_score'] = pd.to_numeric(df['sentiment_score'], errors='coerce')

# Drop any rows with invalid or NaN sentiment scores
df.dropna(subset=['sentiment_score'], inplace=True)

# Convert the 'timestamp' column to datetime if it's not already in datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Set the 'timestamp' as the index for easy time-based analysis
df.set_index('timestamp', inplace=True)

# Verify the sentiment_score column is numeric and check the dtype
print(df['sentiment_score'].dtype)

# Resample only the 'sentiment_score' column and calculate the mean
df_resampled = df['sentiment_score'].resample(time_interval).mean()
df_resampled = df_resampled.apply(lambda x: categorize_sentiment(x))
mean_scores_over_time = df['sentiment_score'].resample(time_interval).mean()


# Drop NaN values from the mean_scores_over_time DataFrame
cleaned_mean_scores = mean_scores_over_time.dropna()
print(cleaned_mean_scores)

# Drop rows with NaN sentiment scores that may result from resampling
#df_resampled.dropna(subset=['sentiment_score'], inplace=True)
#df_resampled.to_csv('test.csv', index=True)
# Check if any data exists in the cleaned_mean_scores_over_time DataFrame
if not cleaned_mean_scores.empty:
    # Plot the sentiment over time using the mean scores
    plt.figure(figsize=(10, 6))
    plt.plot(cleaned_mean_scores.index, cleaned_mean_scores, label='Average Sentiment', color='b')

    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Sentiment Score')
    plt.title(f'Sentiment Over Time for {celebrity_name} on Reddit')
    plt.axhline(0, color='black', linewidth=1)  # Horizontal line at 0 (neutral sentiment)
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print("No valid sentiment data available for plotting.")


# Calculate the percentage of positive, negative, and neutral sentiments over time
sentiment_counts = df_resampled.value_counts()
print(sentiment_counts)

# Plot sentiment counts over time
sentiment_counts.plot(kind='bar', figsize=(8, 6), title="Sentiment Distribution")
plt.xlabel('Sentiment Category')
plt.ylabel('Frequency')
plt.show()
