from threading import Thread
import logging

from nlp.nlp import NLPFactory, NLPResponseError
import actions.action_handler


logger = logging.getLogger(__name__)


class MessageProcessor(Thread):
    def __init__(self, message):
        self.message = message
        Thread.__init__(self)
        self.nlp = NLPFactory().create()
        self.action_handler = actions.action_handler.ActionHandler()

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
