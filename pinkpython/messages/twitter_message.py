from messages.message import Message
from channels.channel import TWITTER


class TwitterMessage(Message):
    def __init__(self, text, original):
        Message.__init__(self, text, channel=TWITTER)
        self.original = original
        self.username = self.original.user.screen_name
        self.reply_id = self.original.id

    def get_reply(self):
        return self.reply_id, self.__build_tweet()

    def __build_tweet(self):
        return '@{0} {1}'.format(self.username, self.text)
