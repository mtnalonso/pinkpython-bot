from queue import Queue
from threading import Thread
from time import sleep

import messages.message_processor


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
        processor = messages.message_processor.MessageProcessor(message)
        processor.start()

    def stop(self):
        self.running = False
