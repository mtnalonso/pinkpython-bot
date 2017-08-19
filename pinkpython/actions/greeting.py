from actions.action import Action
from random import randrange


responses = [
    'FEED MEEE!!',
    'meh',
    'I have an anti-stress pinapple toy'
]


class Greeting(Action):
    def __init__(self):
        pass

    def execute(self, params={}):
        pass

    def get_response_message(self):
        index = randrange(len(responses))
        return responses[index]
