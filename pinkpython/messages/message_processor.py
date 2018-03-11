from threading import Thread
import logging

from nlp.nlp import NLPResponseError


logger = logging.getLogger(__name__)


class MessageProcessor(Thread):
    def __init__(self, message, nlp, action_handler):
        self.message = message
        self.nlp = nlp
        self.action_handler = action_handler
        Thread.__init__(self)

    def run(self):
        logger.info('[Processing]: ' + self.message.text)
        self.execute_nlp()
        self.execute_action()
        return

    def execute_nlp(self):
        try:
            self.message = self.nlp.process(self.message)
        except NLPResponseError as error:
            logger.error(error.message)

    def execute_action(self):
        self.action_handler.process_message(self.message)
