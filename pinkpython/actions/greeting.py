from random import randrange
from actions.action import Action


responses = [
    'FEED MEEE!!',
    'meh',
    'I have an anti-stress pinapple toy'
]


class Greeting(Action):
    def __init__(self, responses=responses):
        self.responses = responses

    def execute(self, params=None):
        pass

    def get_response_message(self):
        index = randrange(len(self.responses))
        return self.responses[index]

