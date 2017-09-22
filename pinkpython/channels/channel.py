from abc import ABC, abstractmethod


TWITTER = 'twitter'
TELEGRAM = 'telegram'
SHELL = 'shell'


class Channel(ABC):
    def __init__(self, inbox_queue):
        if inbox_queue is None:
            raise TypeError('inbox_queue cannot be None')
        self.inbox_queue = inbox_queue
        self.active = False

    @abstractmethod
    def send_reply(self):
        pass

    @abstractmethod
    def init_listener(self):
        pass

    @abstractmethod
    def stop_listener(self):
        pass


class ChannelFactory:
    from channels.twitter_channel import TwitterChannel
    from channels.telegram_channel import TelegramChannel
    from channels.shell_channel import ShellChannel

    CHANNELS = {
        TWITTER: TwitterChannel,
        TELEGRAM: TelegramChannel,
        SHELL: ShellChannel,
    }

    @staticmethod
    def create(channel_name, inbox_queue):
        channel = ChannelFactory.CHANNELS.get(channel_name)
        return channel(inbox_queue)
