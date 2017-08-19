from pprint import pprint
import tweepy
from configparser import ConfigParser
from credentials import consumer_key, consumer_secret, access_token, \
        access_token_secret


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

config = ConfigParser()
config.read('pinkpython.conf')
twitter_account = config.get('twitter', 'username')

def put_tweet(tweet):
    api.update_status(status=tweet)

def send_response(message):
    reply_id, tweet = message.get_tweet_reply()
    api.update_status(tweet, reply_id)

def init_twitter_listener():
    listener = TwitterListener()
    stream = tweepy.Stream(auth=auth, listener=listener)
    stream.filter(track=[twitter_account], async=True)

if __name__ == '__main__':
    from inbox import TwitterListener, InboxConsumer
    from outbox import OutboxConsumer
    init_twitter_listener()
    inbox_consumer = InboxConsumer()
    outbox_consumer = OutboxConsumer()
    inbox_consumer.start()
    outbox_consumer.start()
