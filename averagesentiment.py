import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Authenticate with Reddit API
reddit = praw.Reddit(
    client_id='7m09T71RyrT9PuWpfrXEjg',
    client_secret='FCMgp8KgX3MIdw4Cpw1wg3h9AQTy8g',
    user_agent='Unfair-Suggestion-19'

)

# Initialize VADER SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Sentiment analysis function
def analyze_sentiment(text):
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']  # compound score gives the overall sentiment

# Replace with the actual submission ID
submission = reddit.submission(id='1jmybws')

# Get all comments in the submission (including nested comments)
submission.comments.replace_more(limit=0)  # Prevent PRAW from truncating comments

# Variables to store the sum of sentiment scores and the number of comments
total_sentiment = 0
comment_count = 0

# Loop through comments and calculate sentiment scores
for comment in submission.comments.list():
    # Get the text of the comment
    comment_text = comment.body
    
    # Perform sentiment analysis on the comment
    sentiment_score = analyze_sentiment(comment_text)
    
    # Accumulate the sentiment score
    total_sentiment += sentiment_score
    comment_count += 1

# Calculate the average sentiment if there are comments
if comment_count > 0:
    average_sentiment = total_sentiment / comment_count
    #print(f"Average Sentiment Score: {average_sentiment}")
else:
    print("No comments found.")
def categorize_sentiment(compound_score):
    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Calculate average sentiment and categorize it
if comment_count > 0:
    average_sentiment = total_sentiment / comment_count
    sentiment_category = categorize_sentiment(average_sentiment)
    print(f"Average Sentiment: {sentiment_category} (Score: {average_sentiment}) (Comment count: {comment_count})")
else:
    print("No comments found.")

