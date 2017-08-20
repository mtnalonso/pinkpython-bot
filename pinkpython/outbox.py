from queue import Queue
from threading import Thread
from time import sleep
import logging

import channels.twitter


logger = logging.getLogger(__name__)


outbox_queue = Queue()


class OutboxConsumer(Thread):
    def __init__(self, outbox_queue=outbox_queue):
        self.outbox_queue = outbox_queue
        self.running = True
        self.twitter_channel = channels.twitter.twitter_channel
        Thread.__init__(self)

    def run(self):
        while self.running:
            self.__process_next_message()
        return

    def __process_next_message(self):
        message = self.__read_next_message()
        if message is not None:
            self.__send_message(message)
        sleep(1)

    def __read_next_message(self):
        return self.outbox_queue.get()

    def __send_message(self, message):
        # TODO process message according to class (twitter/telegram)
        # and send response
        logger.info('[Outbox]: ' + str(message))
        self.__send_twitter_response(message)

    def __send_twitter_response(self, message):
        self.twitter_channel.send_response(message)

    def stop(self):
        self.running = False
