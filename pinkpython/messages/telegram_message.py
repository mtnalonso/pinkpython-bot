from messages.message import Message
from channels.channel import TELEGRAM


class TelegramMessage(Message):
    def __init__(self, update):
        Message.__init__(self, update.message.text, channel=TELEGRAM)
        self.udpate = update
        self.original = update.message
        self.username = update.message.from_user.username
        self.chat_id = update.message.chat_id

    def get_reply(self):
        return self.__build_reply()

    def __build_reply(self):
        return '@{0} {1}'.format(self.username, self.text)
