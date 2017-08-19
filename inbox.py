from queue import Queue
from threading import Thread
from time import sleep
import logging

import tweepy

from nlp import NLPFactory, NLPResponseError
from model.message import Message
from actions.action_handler import ActionHandler


logging.basicConfig(filename='python_memories.log', filemode='w',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

inbox_queue = Queue()


class MessageProcessor(Thread):
    def __init__(self, message):
        self.message = message
        Thread.__init__(self)
        self.nlp = NLPFactory().create()
        self.action_handler = ActionHandler()

    def run(self):
        logger.info('[Processing]: ' + self.message.text)
        self.execute_nlp()
        self.execute_action()
        return

    def execute_nlp(self):
        try:
            self.message = self.nlp.process(self.message)
        except NLPResponseError:
            raise NotImplementedError

    def execute_action(self):
        self.action_handler.process_message(self.message)


class InboxConsumer(Thread):
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
        message = Message(status.text, platform='twitter', original=status)
        self.queue.put(message)

    def on_error(self, status_code):
        print('ERROR', status_code)
        if status_code == 420:
            logger.error("[420]:\tEnhance Your Calm!")
            return False
