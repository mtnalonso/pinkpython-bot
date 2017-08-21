from queue import Queue
from threading import Thread
from time import sleep

from messages.message_processor import MessageProcessor


class InboxConsumer(Thread):
    """
    Get tweets from the inbox queue and process each one in a new thread
    """
    def __init__(self, inbox_queue, outbox_queue):
        self.inbox_queue = inbox_queue
        self.running = True
        self.outbox_queue = outbox_queue
        Thread.__init__(self)

    def run(self):
        while self.running:
            self.process_next_message()
        return

    def process_next_message(self):
        if not self.inbox_queue.empty():
            self.process_message()
        sleep(1)

    def process_message(self):
        message = self.inbox_queue.get()
        processor = MessageProcessor(message, self.outbox_queue)
        processor.start()

    def stop(self):
        self.running = False
