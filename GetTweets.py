# Imports
from tweepy import API 
from tweepy import Cursor
from tweepy import OAuthHandler
import json
import preprocessor as p
import authentification
import sys

# Twitter Authenticator - Connect with the twitter API
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(authentification.consumer_key, authentification.consumer_secret)
        auth.set_access_token(authentification.access_token, authentification.access_token_secret)
        
        return auth
      
# Twitter Client - Download a certain number of tweets from a twitter-timeline 
class TwitterClient():
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)


    def get_user_timeline_tweets(self, user, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, user).items(num_tweets):
            tweets.append(tweet)
            
        return tweets
    
#Tweet Preprocessor - Preprocessing the tweet for further processing
class TweetPreprocessor():
    
    def preprocessor(self, tweet):

        # Replace umlauts
        tweet = tweet.replace("\u00e4", "ae")
        tweet = tweet.replace("\u00f6", "oe")
        tweet = tweet.replace("\u00fc", "ue")
        tweet = tweet.replace("\u00df", "ss")
        tweet = tweet.replace("\u00c4","Ae")
        tweet = tweet.replace("\u00d6","Oe")
        tweet = tweet.replace("\u00dc","Ue")
        
        # Remove # and @
        tweet = tweet.replace("@", "")
        tweet = tweet.replace("#", "")
        tweet = tweet.replace("_"," ")
        
        # separates camelcase notation with spaces
        for i in range(0, len(tweet)):
            if tweet[i].isupper() and tweet[i-1].islower():
                tweet = tweet[:i] + ' ' + tweet[i:]
                
        # Remove url, emoji, smiley; convert to ascii
        p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.SMILEY)
        tweet = p.clean(tweet)
        tweet = str(tweet.encode("ascii", "ignore"))
        tweet = tweet.replace("b'","")
        return tweet

# Tweet Analyzer - Returns the required information of the tweet   
class TweetAnalyzer():
    
    def tweets_Array(self, tweets):
        tweetsarray = []
        for tweet in tweets:
            text = tweet_preprocessor.preprocessor(tweet.text)
            createdAt = tweet.created_at
            author = tweet.author
            name = author.name
            coordinates = tweet.coordinates
            array = [text, createdAt, name, coordinates]
            tweetsarray.append(array)
            
        return tweetsarray

# Text Writer - Writes the required information of the tweet into a file   
class TextWriter():
    def jsonFile(self,tweetsarray):
        fileLocation = open("tweets.txt", "w")
        # Transfers tweet to json format
        for tweet in tweetsarray:
            entry = {
                "text": str(tweet[0]),
                "date": str(tweet[1]),
                "author": str(tweet[2]),
                "coordinates": str(tweet[3])
                }
            jsonEntry = json.dumps(entry)

            # Write in File
            fileLocation.write(jsonEntry + "\n")
        fileLocation.close()
        
        return "True"
    
# Main-Methode
if __name__ == '__main__':
    
    try:
        # Create class objects
        twitter_client = TwitterClient()
        tweet_preprocessor = TweetPreprocessor()
        tweet_analyzer = TweetAnalyzer()
        text_writer = TextWriter()

        # Transferring the settings to get the tweets
        anzahl = int(sys.argv[2])
        tweets = twitter_client.get_user_timeline_tweets(sys.argv[1], anzahl)
    
        # Use the functions to write the required information of the tweets into a file
        tweetsarray = tweet_analyzer.tweets_Array(tweets)
        fileLocation = text_writer.jsonFile(tweetsarray)
    
    except (Exception) as error :
        print("Tweets konnten nicht geladen werden")
    
