from abc import ABC, abstractmethod


TWITTER = 'twitter'
TELEGRAM = 'telegram'


class Channel(ABC):
    def __init__(self, inbox_queue):
        if inbox_queue is None:
            raise TypeError('inbox_queue cannot be None')
        self.inbox_queue = inbox_queue

    @abstractmethod
    def send_message(self):
        pass

    @abstractmethod
    def send_reply(self):
        pass

    @abstractmethod
    def init_listener(self):
        pass


class ChannelFactory:
    from channels.twitter_channel import TwitterChannel
    from channels.telegram_channel import TelegramChannel

    CHANNELS = {
        TWITTER: TwitterChannel,
        TELEGRAM: TelegramChannel
    }

    @staticmethod
    def create(channel_name, inbox_queue):
        channel = ChannelFactory.CHANNELS.get(channel_name)
        return channel(inbox_queue)
