from abc import ABC, abstractmethod


class Action(ABC):
    def __init__(self):
        self.params = {}

    @abstractmethod
    def execute(self, params={}):
        pass

    @abstractmethod
    def get_response_message(self):
        pass
