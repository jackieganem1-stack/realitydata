import praw
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import math
import time

# Optional: Categorize sentiment as Positive, Negative, or Neutral
def categorize_sentiment(compound_score):
    if not math.isnan(compound_score):
        if compound_score > 0.05:
            return "Positive"
        elif compound_score < -0.05:
            return "Negative"
        else:
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
celebrity_name = 'Julia'

# Define the time interval for sampling (e.g., '1D' for daily intervals)
time_interval = '1W'  # '1H' for hourly, '1D' for daily, etc.

# Search for posts/comments mentioning the celebrity name
subreddit = reddit.subreddit('dancingwiththestars')  # Search across all subreddits

# Fetch posts or comments mentioning the celebrity
#mentions = subreddit.search(celebrity_name, sort='new')  # Adjust the limit as needed

# List to store sentiment data
sentiment_data = []

# Set the time range for data collection
start_date = datetime.datetime(2025, 12, 1)  # Example: Start from January 1, 2023
end_date = datetime.datetime(2025, 12, 31)  # Example: End on December 31, 2023

# Set a time interval for fetching (e.g., 1 week)
time_delta = datetime.timedelta(weeks=1)

# Fetch data for each time period (e.g., each week)
current_start_date = start_date
while current_start_date < end_date:
    current_end_date = current_start_date + time_delta
    print(f"Fetching data from {current_start_date} to {current_end_date}")

    # Fetch posts within the time range
    # Fetch posts between the specified start_time and end_time
    mentions = subreddit.search(celebrity_name, sort='new', time_filter='all', limit=1000)
    # Loop through the search results (posts and comments)
    for mention in mentions:
        # Construct mention_text based on available attributes
        mention_text = mention.title + " " + (mention.selftext if hasattr(mention, 'selftext') else "")
        # Perform sentiment analysis on the mention text
        sentiment_score = analyze_sentiment(mention_text)
        # Get the timestamp of the post or comment
        post_timestamp = datetime.datetime.utcfromtimestamp(mention.created_utc)
        start_time = datetime.datetime(2023, 12, 1)
        end_time = datetime.datetime(2024, 12, 1)
        if start_time <= post_timestamp <= end_time:
            # Get the text of the post or comment
            #mention_text = mention.title + " " + mention.selftext if hasattr(mention, 'selftext') else mention.body
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
            print("Invalid sentiment score, not appending to list") # Check if score is invalid
    # Update the start date for the next iteration
    current_start_date = current_end_date

    # To avoid hitting Reddit's rate limit, sleep for a few seconds
    time.sleep(7)


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
df_to_csv = df
# Resample only the 'sentiment_score' column and calculate the mean
df_resampled = df['sentiment_score'].resample(time_interval).mean()
df_resampled = df_resampled.apply(lambda x: categorize_sentiment(x))
mean_scores_over_time = df['sentiment_score'].resample(time_interval).mean()


# Drop NaN values from the mean_scores_over_time DataFrame
cleaned_mean_scores = mean_scores_over_time.dropna()
print(cleaned_mean_scores)
print('_________')
clean_df = cleaned_mean_scores
clean_df.to_csv('scores_file.csv', index=True)


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
    plt.title(f'Sentiment Over Time for {celebrity_name} in {subreddit}')
    plt.axhline(0, color='black', linewidth=1)  # Horizontal line at 0 (neutral sentiment)
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print("No valid sentiment data available for plotting.")

df_to_csv.to_csv('new_file.csv', index=False)
# Calculate the percentage of positive, negative, and neutral sentiments over time
sentiment_counts = df_resampled.value_counts()
print(sentiment_counts)

# Plot sentiment counts over time
sentiment_counts.plot(kind='bar', figsize=(8, 6), title="Sentiment Distribution")
plt.xlabel('Sentiment Category')
plt.ylabel('Frequency')
plt.show()

