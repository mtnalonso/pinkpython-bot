from pprint import pprint
import tweepy
from credentials import consumer_key, consumer_secret, access_token, \
        access_token_secret


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def put_tweet(tweet):
    api.update_status(status=tweet)

def send_response(message):
    reply_id, tweet = message.get_tweet_reply()
    api.update_status(tweet, reply_id)

def init_twitter_listener():
    listener = TwitterListener()
    stream = tweepy.Stream(auth=auth, listener=listener)
    stream.filter(track=['pinkpythonbot'], async=True)

if __name__ == '__main__':
    from inbox import TwitterListener, InboxConsumer
    init_twitter_listener()
    consumer = InboxConsumer()
    consumer.start()
