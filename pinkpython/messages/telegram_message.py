from messages.message import Message
from channels.channel import TELEGRAM


class TelegramMessage(Message):
    def __init__(self, text):
        Message.__init__(self, text, channel=TELEGRAM)
        pass

    def get_reply(self):
        return self.text
