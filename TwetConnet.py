import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterAnalysisApi(object):
    def __init__(self):

        #twitter api keys enter
        consumer_key = 'I9w8G5ZYp1Yjcqz5NWBqg'
        consumer_secret = 'UHeWUjEzhqOEJhY4WZOjWOLYFuPUdhKsGji9OpcxlY'
        access_token = '65599565-pqwgb4stWGfqLMw8UVlfZFOu5901v9dOlFPXR65MN'
        access_token_secret = 'S84i48lyYCz7rifBjaXLmCDvrX4CtB677uUkNuAm2HCa6'
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        # using textblob's sentiment method
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query,result_type = "recent",lang = "en", count=count, tweet_mode="extended")

            # parsing
            for tweet in fetched_tweets:
                parsed_tweet = {}
                #print(tweet.full_text)
                #print(self.clean_tweet(tweet.full_text))
                # saving text of tweet
                parsed_tweet['ham'] = tweet.full_text
                parsed_tweet['text'] = self.clean_tweet(tweet.full_text)
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets


        except tweepy.TweepError as e:
            print("Error : " + str(e))
