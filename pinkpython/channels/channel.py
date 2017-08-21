from abc import ABC, abstractmethod


class Channel(ABC):
    def __init__(self, inbox_queue):
        self.inbox_queue = inbox_queue

    @abstractmethod
    def send_message(self):
        pass


class ChannelFactory:
    from channels.twitter_channel import TwitterChannel
    from channels.telegram_channel import TelegramChannel

    CHANNELS = {
        'twitter': TwitterChannel,
        'telegram': TelegramChannel
    }

    @staticmethod
    def create(channel_name, inbox_queue):
        channel = ChannelFactory.CHANNELS.get(channel_name)
        return channel(inbox_queue)
