import logging
from random import choice
from actions.action import Action


logger = logging.getLogger(__name__)

responses = [
    'yum-yum',
    'such delicious {0}',
    'yay {0}'
]


class Feed(Action):
    def __init__(self, responses=responses):
        Action.__init__(self)
        self.responses = responses
        self.params = None
        self.food = None

    def execute(self, params=None):
        self.__process_params(params)

    def get_response_message(self):
        return choice(self.responses).format(self.food)

    def __process_params(self, params):
        self.params = params
        self.food = self.params['food'][0]
        logger.info('[ACTION:feed]:\tFedding with ' + self.food)
