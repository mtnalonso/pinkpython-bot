from threading import Thread
import logging

from nlp.nlp import NLPFactory, NLPResponseError
from actions.action_handler import ActionHandler


logging.basicConfig(filename='python_memories.log', filemode='w',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageProcessor(Thread):
    def __init__(self, message):
        self.message = message
        Thread.__init__(self)
        self.nlp = NLPFactory().create()
        self.action_handler = ActionHandler()

    def run(self):
        logger.info('[Processing]: ' + self.message.text)
        self.execute_nlp()
        self.execute_action()
        return

    def execute_nlp(self):
        try:
            self.message = self.nlp.process(self.message)
        except NLPResponseError:
            raise NotImplementedError

    def execute_action(self):
        self.action_handler.process_message(self.message)
