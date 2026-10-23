import praw
from textblob import TextBlob

# Authenticate with Reddit API
reddit = praw.Reddit(
    client_id='7m09T71RyrT9PuWpfrXEjg',
    client_secret='FCMgp8KgX3MIdw4Cpw1wg3h9AQTy8g',
    user_agent='Unfair-Suggestion-19'
)
'''
# Choose the subreddit you want to scrape
subreddit = reddit.subreddit('learnpython')

# Scrape the 10 most recent posts
for submission in subreddit.new(limit=10):
    print(f"Title: {submission.title}")
    print(f"Text: {submission.selftext}")
    print(f"URL: {submission.url}")
    print("------------")
'''
submission = reddit.submission(id='1jlo1ez')  # Replace with the actual submission ID
submission.comments.replace_more(limit=0)  # Prevent PRAW from truncating comments

for comment in submission.comments.list():
    print(f"Comment: {comment.body}")
    print("------------")

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # Returns a value between -1 (negative) and 1 (positive)
    return sentiment

# Example: Analyzing the sentiment of a Reddit post's title
for submission in subreddit.new(limit=10):
    title = submission.title
    sentiment = analyze_sentiment(title)
    print(f"Title: {title}")
    print(f"Sentiment: {sentiment}")
    print("------------")

