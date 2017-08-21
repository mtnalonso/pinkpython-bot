from abc import ABC, abstractmethod


class Channel(ABC):
    def __init__(self, inbox_queue):
        if inbox_queue is None:
            raise TypeError('inbox_queue cannot be None')
        self.inbox_queue = inbox_queue

    @abstractmethod
    def send_message(self):
        pass

    @abstractmethod
    def init_listener(self):
        pass

class ChannelSingletonFactory:
    from channels.twitter_channel import TwitterChannel
    from channels.telegram_channel import TelegramChannel

    CHANNELS = {
        'twitter': TwitterChannel,
        'telegram': TelegramChannel
    }

    @staticmethod
    def get_instance(channel_name, inbox_queue):
        if str(channel_name + '*') in ChannelSingletonFactory.CHANNELS:
            return ChannelSingletonFactory.CHANNELS.get(channel_name + '*')

        channel = ChannelSingletonFactory.CHANNELS.get(channel_name)
        channel_instance = channel(inbox_queue)
        ChannelSingletonFactory.CHANNELS[channel_name+'*'] = channel_instance
        return channel_instance
