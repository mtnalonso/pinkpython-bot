from queue import Queue
from threading import Thread
from time import sleep

import twitter_snake as twitter_connector


outbox_queue = Queue()


class OutboxConsumer(Thread):
    def __init__(self, queue=outbox_queue):
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
        return self.queue.get()

    def __send_message(self, message):
        # TODO process message according to class (twitter/telegram)
        # and send response
        print('OUTPUT')
        print(str(message))
        # self.__send_twitter_response(message)

    def __send_twitter_response(self, message):
        self.twitter_connector.send_response(message)

    def stop(self):
        self.running = False
