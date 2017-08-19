from random import randrange
from actions.action import Action


responses = [
    'yum-yum',
    'such delicious {0}',
    'yay {0}'
]


class Feed(Action):
    def __init__(self):
        Action.__init__(self)
        self.food = None

    def execute(self, params={}):
        self.__process_params(params)

    def get_response_message(self):
        index = randrange(len(responses))
        return responses[index].format(self.food)

    def __process_params(self, params):
        self.params = params
        self.food = self.params['food'][0]
