from random import randrange
from actions.action import Action


responses = [
    'WHAT?!',
    'I DONT UNDERSSTAND YOU!'
]


class Error(Action):
    def __init__(self, responses=responses):
        self.responses = responses

    def execute(self, params=None):
        pass

    def get_response_message(self):
        index = randrange(len(self.responses))
        return self.responses[index]

