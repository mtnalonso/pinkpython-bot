from abc import ABC
from random import choice


class Action(ABC):
    def __init__(self, params=None, responses=None):
        self.params = {}
        self.responses = ['']

    def execute(self, params=None):
        pass

    def get_response_message(self):
        return choice(self.responses)

