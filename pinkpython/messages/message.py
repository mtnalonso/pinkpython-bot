from abc import abstractmethod


class Message:
    def __init__(self, text, channel=None):
        self.text = text
        self.query = text
        self.action = None
        self.parameters = {}
        self.channel = channel

    def __repr(self):
        return 'Message({!r}, {!r}'.format(self.text, self.channel)

    def __str__(self):
        msg_str = 'action\t{0}\nquery\t{1}\nparams\t{2}\ntext\t{3}\n\t{4}'
        return msg_str.format(
            self.action, self.query, self.parameters, self.text, self.channel
        )

    @abstractmethod
    def get_reply(self):
        pass
