from queue import Queue
from threading import Thread
from time import sleep

import twitter_snake


outbox_queue = Queue()


class Outbox(Thread):
    def __init__(self, queue=outbox_queue):
        self.queue = queue
        self.running = True
        Thread.__init__(self)

    def run(self):
        while self.running:
            self.__send_next_message()
            sleep(1)
        return

    def put_message(self, message):
        self.queue.put(message)

    def __send_next_message(self):
        if not self.queue.empty():
            message = self.queue.get()
            self.__send_message(message)

    def _send_twitter_response(self, message):
        twitter_snake.send_response(message)

    def __send_message(self, message):
        # TODO process message according to class (twitter/telegram)
        # and send response
        self._send_twitter_response(message)

    def stop(self):
        self.running = False
