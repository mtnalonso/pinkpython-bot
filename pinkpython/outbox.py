from threading import Thread
from time import sleep
import logging


logger = logging.getLogger(__name__)


class OutboxConsumer(Thread):
    def __init__(self, outbox_queue, broadcaster):
        self.outbox_queue = outbox_queue
        self.running = True
        self.broadcaster = broadcaster
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
        logger.info('[Outbox]:\n\n' + str(message) + '\n')
        self.broadcaster.send_message(message)

    def stop(self):
        self.running = False
