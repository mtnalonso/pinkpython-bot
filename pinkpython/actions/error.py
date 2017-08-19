from actions.action import Action
from random import randrange


responses = [
    'WHAT?!',
    'I DONT UNDERSSTAND YOU!'
]


class Error(Action):
    def __init__(self):
        pass

    def execute(self, params={}):
        pass

    def get_response_message(self):
        index = randrange(len(responses))
        return responses[index]
