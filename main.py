import tweepy
from textblob import TextBlob

# Credentials
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

list_contains_sentiment = []  # A list that stores sentiments of all tweets

def scrape_hashtags(query, count=5):
    hashtags = []

    for tweet in tweepy.Cursor(api.search_tweets, q=query, tweet_mode='extended').items(count):
        for hashtag in tweet.entities['hashtags']:
            hashtags.append(hashtag['text'].lower())

    return hashtags

def analyze_sentiment(tweet_text):
    analysis = TextBlob(tweet_text)
    sentiment_polarity = analysis.sentiment.polarity

    if sentiment_polarity > 0:
        return "Positive"
    elif sentiment_polarity < 0:
        return "Negative"
    else:
        return "Neutral"

if __name__ == "__main__":
    hashtag_query = '#google'
    count_to_scrape = 200  # Number of tweets to scrape

    hashtags_list = scrape_hashtags(hashtag_query, count_to_scrape)

    for hashtag in hashtags_list:
        print(f"Scraping tweets with the hashtag: {hashtag}")
        tweets = scrape_hashtags(hashtag, count_to_scrape)
        if len(tweets) > 0:
            print(f"Sentiment analysis for hashtag '{hashtag}':")
            for tweet in tweets:
                sentiment = analyze_sentiment(tweet)
                list_contains_sentiment.append(sentiment)  # Add the sentiment to the list
                print(f"Tweet: '{tweet}' - Sentiment: {sentiment}")
        else:
            print(f"No tweets found for hashtag '{hashtag}'.")

    # Print the list containing all sentiments
    print("List of Sentiments:", list_contains_sentiment)

    positive_count = list_contains_sentiment.count('Positive')
    negative_count = list_contains_sentiment.count('Negative')
    neutral_count = list_contains_sentiment.count('Neutral')
    total_tweets = len(list_contains_sentiment)
    print(len(list_contains_sentiment))

    print("\nSentiment Analysis Summary:")
    print(f"Total Tweets: {total_tweets}")
    print(f"Positive Tweets: {positive_count}")
    print(f"Negative Tweets: {negative_count}")
    print(f"Neutral Tweets: {neutral_count}")

    positive_percentage = (positive_count / total_tweets) * 100
    negative_percentage = (negative_count / total_tweets) * 100
    neutral_percentage = (neutral_count / total_tweets) * 100

    print(f"\nPercentage of Positive Tweets: {positive_percentage:.2f}%")
    print(f"Percentage of Negative Tweets: {negative_percentage:.2f}%")
    print(f"Percentage of Neutral Tweets: {neutral_percentage:.2f}%")

    if positive_percentage > 50:
        print("\nThe sentiment around the product appears to be mostly positive.")
    elif negative_percentage > 50:
        print("\nThe sentiment around the product appears to be mostly negative.")
    else:
        print("\nThe sentiment around the product appears to be neutral or balanced.")
