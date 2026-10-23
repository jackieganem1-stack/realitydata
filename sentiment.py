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
submission = reddit.submission(id='1jlo1ez')

# Get all comments in the submission (including nested comments)
submission.comments.replace_more(limit=0)  # Prevent PRAW from truncating comments

# Loop through comments and print sentiment data
for comment in submission.comments.list():
    # Get the text of the comment
    comment_text = comment.body
    
    # Perform sentiment analysis on the comment
    sentiment_score = analyze_sentiment(comment_text)
    
    # Print comment and its sentiment score
    #print(f"Sentiment Score: {sentiment_score}")
    #print("------------")

def categorize_sentiment(compound_score):
    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Loop through comments and categorize sentiment
for comment in submission.comments.list():
    comment_text = comment.body
    sentiment_score = analyze_sentiment(comment_text)
    sentiment_category = categorize_sentiment(sentiment_score)
    
    print(f"Sentiment: {sentiment_category} (Score: {sentiment_score})")
    print("------------")

