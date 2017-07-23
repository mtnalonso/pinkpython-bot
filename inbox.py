from queue import Queue
from threading import Thread
from time import sleep
import logging

import tweepy

from nlp import NLPFactory
from twitter_snake import send_response


logging.basicConfig(filename='python_memories.log', level=logging.INFO)

inbox_queue = Queue()


class Message:
    """
    Message format to send over processors
     - text:        original message text
     - original:    twitter / telegram message class
    """
    def __init__(self, text, original=None):
        self.text = text
        self.original = original

    def __repr__(self):
        raise NotImplementedError


class MessageProcessor(Thread):
    def __init__(self, message):
        self.message = message
        Thread.__init__(self)
        self.nlp = NLPFactory().create()

    def run(self):
        logger.info('[Processing]: ' + self.message.text)
        nlp_response = self.request_nlp_response()
        send_response(nlp_response, self.message.original)
        return

    def request_nlp_response(self):
        try:
            nlp_response = self.nlp.process(self.message.text)
        except NLPResponseError:
            raise NotImplementedError
        return nlp_response


class MessageConsumer(Thread):
    """
    Get tweets from the inbox queue and process each one in a new thread
    """
    def __init__(self, queue=inbox_queue):
        self.queue = queue
        self.running = True
        Thread.__init__(self)

    def run(self):
        while self.running:
            self.check_queue()
            sleep(1)
        return

    def check_queue(self):
        if not self.queue.empty():
            self.process_message()

    def process_message(self):
        message = self.queue.get()
        processor = MessageProcessor(message)
        processor.start()

    def stop(self):
        self.running = False


class TwitterListener(tweepy.StreamListener):
    """
    Stream twitter mentions and put each mention message in the inbox queue
    """
    def __init__(self, queue=inbox_queue):
        super().__init__()
        self.queue = queue

    def on_status(self, status):
        logger.info('@[' + status.user.screen_name + ']:' + status.text)
        message = Message(status.text, status)
        inbox_queue.put(message)

    def on_error(self, status_code):
        print('ERROR', status_code)
        if status_code == 420:
            logger.error("[420]:\tEnhance Your Calm!")
            return False
