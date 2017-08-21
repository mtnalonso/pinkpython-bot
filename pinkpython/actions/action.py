from abc import ABC
from random import randrange


class Action(ABC):
    def __init__(self, params=None, responses=None):
        self.params = {}
        self.responses = ['']

    def execute(self, params=None):
        pass

    def get_response_message(self):
        index = randrange(len(self.responses))
        return self.responses[index]
