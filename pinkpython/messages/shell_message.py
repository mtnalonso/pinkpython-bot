from messages.message import Message
from channels.channel import SHELL


class ShellMessage(Message):
    def __init__(self, message):
        Message.__init__(self, message, channel=SHELL)

    def get_reply(self):
        return self.text
