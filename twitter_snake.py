from pprint import pprint
import tweepy
from credentials import consumer_key, consumer_secret, access_token, \
        access_token_secret


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def put_tweet(tweet):
    api.update_status(status=tweet)

def send_response(message, status):
    tweet_id = status.id
    response = ('@' + status.user.screen_name + ' '
                + message.generated_response)
    api.update_status(response, tweet_id)

def init_twitter_listener():
    listener = TwitterListener()
    stream = tweepy.Stream(auth=auth, listener=listener)
    stream.filter(track=['pinkpythonbot'], async=True)

if __name__ == '__main__':
    from inbox import TwitterListener, MessageConsumer
    init_twitter_listener()
    consumer = MessageConsumer()
    consumer.start()
