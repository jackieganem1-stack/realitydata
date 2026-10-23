import praw
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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
# Change to the celebrity you're interested in

# Search for posts/comments mentioning the celebrity name
subreddit = reddit.subreddit('all')  # Search across all subreddits

# Fetch posts or comments mentioning the celebrity
mentions = subreddit.search(celebrity_name, sort = 'new', limit = 250)  # Adjust the limit as needed

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

if 'timestamp' in df.columns:
    # Convert 'timestamp' column to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    print('YES')
else:
    print("Error: 'timestamp' column not found.")

# Now set 'timestamp' as the index if it's available
if 'timestamp' in df.columns:
    df.set_index('timestamp', inplace=True)
    print('YES')
else:
    print("Error: 'timestamp' column missing, cannot set as index.")


print(post_timestamp)


# Convert the 'timestamp' column to datetime if it's not already in datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Set the 'timestamp' as the index for easy time-based analysis
df.set_index('timestamp', inplace=True)

df['timestamp'] = pd.to_datetime(df['timestamp']) # makes the column a datetime column, needed for resample
df = df.set_index('timestamp')
df_grp = df.groupby('sentiment_score').resample('h').sum()
print(df_grp)
print('_________')
# Show the first few rows of the DataFrame to check the data
#print(df.head())
#print(df.to_string())
#print(df.head())
df_sorted = df.sort_values(by='timestamp')
df_sorted.to_csv('test.csv', index=True)
df_resampled = df_sorted
time_interval = 'D'
#df_resampled = df.resample(time_interval).sum()
# Check if any data exists in the resampled DataFrame
if not df_resampled.empty:
    # Plot the sentiment over time
    plt.figure(figsize=(10,6))
    plt.plot(df_resampled.index, df_resampled['sentiment_score'], label='Average Sentiment', color='b')

    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Sentiment Score')
    plt.title(f'Sentiment Over Time for {celebrity_name} on Reddit')
    plt.axhline(0, color='black',linewidth=1)  # Horizontal line at 0 (neutral sentiment)
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print("No valid sentiment data available for plotting.")

# Optional: Categorize sentiment as Positive, Negative, or Neutral
def categorize_sentiment(compound_score):
    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment categorization
df['sentiment_category'] = df['sentiment_score'].apply(categorize_sentiment)

# Calculate the percentage of positive, negative, and neutral sentiments over time
sentiment_counts = df['sentiment_category'].value_counts()
print(sentiment_counts)

# Plot sentiment counts over time
sentiment_counts.plot(kind='bar', figsize=(8,6), title="Sentiment Distribution")
plt.xlabel('Sentiment Category')
plt.ylabel('Frequency')
plt.show()
exit()
