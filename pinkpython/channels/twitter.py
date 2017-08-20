import tweepy
import logging

import config
from inbox import inbox_queue
from messages.message import Message
from credentials import consumer_key, consumer_secret, access_token, \
        access_token_secret


logger = logging.getLogger(__name__)


class TwitterChannel:
    def __init__(self, inbox_queue=inbox_queue):
        self.auth = None
        self.api = None
        self.username = 'pinkpythonbot'

        self.inbox_queue = inbox_queue
        self.listener = None
        self.stream = None

        self.__load_auth()
        self.__load_config()

    def __load_auth(self):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

    def __load_config(self):
        self.username = config.twitter_username

    def put_tweet(self, tweet):
        self.api.update_status(status=tweet)

    def send_response(self, message):
        reply_id, tweet = message.get_tweet_reply()
        logger.info('TWITTER: -> ' + tweet)
        self.api.update_status(tweet, reply_id)

    def init_listener(self):
        self.listener = TwitterListener(self.inbox_queue)
        self.stream = tweepy.Stream(auth=self.auth, listener=self.listener)
        self.stream.filter(track=[self.username], async=True)


class TwitterListener(tweepy.StreamListener):
    """
    Stream twitter mentions and put each mention message in the inbox queue
    """
    def __init__(self, inbox_queue):
        super().__init__()
        self.inbox_queue = inbox_queue

    def on_status(self, status):
        username = status.user.screen_name
        logger.info('TWITTER: @[' + username + ']: ' + status.text)
        message = Message(status.text, platform='twitter', original=status)
        self.inbox_queue.put(message)

    def on_error(self, status_code):
        if status_code == 420:
            logger.error("[420]:\tEnhance Your Calm!")
            return False


twitter_channel = TwitterChannel()


if __name__ == '__main__':
    from inbox import InboxConsumer
    from outbox import OutboxConsumer

    twitter_channel.init_listener()

    inbox_consumer = InboxConsumer()
    outbox_consumer = OutboxConsumer()
    inbox_consumer.start()
    outbox_consumer.start()
