from abc import ABC, abstractmethod


class Message:
    def __init__(self, text, channel=None):
        self.text = text
        self.query = text
        self.action = None
        self.parameters = {}
        self.channel = channel

    def __repr__(self):
        return ('action:\t' + str(self.action) + '\nquery:\t' +
                str(self.query) + '\nparams:\t' + str(self.parameters) +
                '\ntext:\t' + str(self.text))

    @abstractmethod
    def get_reply(self):
        pass
