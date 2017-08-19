from abc import abstractmethod
from queue import Queue
from threading import Thread
from time import sleep

import twitter_snake as twitter_connector

class _Outbox(Queue):
    def __init__(self):
        Queue.__init__(self)

    def put_message(self, message):
        if not self.full():
            self.put(message)

    def get_message(self):
        if not self.empty():
            return self.get()


class OutboxConsumer(Thread):
    def __init__(self, queue):
        self.queue = queue
        self.running = True
        self.twitter_connector = twitter_connector
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
        return self.queue.get_message()

    def __send_message(self, message):
        # TODO process message according to class (twitter/telegram)
        # and send response
        self.__send_twitter_response(message)

    def __send_twitter_response(self, message):
        self.twitter_connector.send_response(message)

    def stop(self):
        self.running = False


outbox = _Outbox()
outbox_consumer = OutboxConsumer(outbox)
outbox_consumer.start()



class QueueConsumer(Thread):
    def __init__(self, queue):
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

    @abstractmethod
    def process_message(self):
        pass

    def stop(self):
        self.running = False
