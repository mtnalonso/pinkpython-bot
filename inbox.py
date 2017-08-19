from queue import Queue
from threading import Thread
from time import sleep

import tweepy

from model.message import Message
from message_processor import MessageProcessor


inbox_queue = Queue()


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
            self.process_next_message()
        return

    def process_next_message(self):
        if not self.queue.empty():
            self.process_message()
        sleep(1)

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
        # logger.info('@[' + status.user.screen_name + ']:' + status.text)
        message = Message(status.text, platform='twitter', original=status)
        self.queue.put(message)

    def on_error(self, status_code):
        print('ERROR', status_code)
        if status_code == 420:
            logger.error("[420]:\tEnhance Your Calm!")
            return False
