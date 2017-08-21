import logging


logger = logging.getLogger(__name__)


class DuplicateChannelError(Exception):
    def __init__(self, channel_name):
        self.message = 'Channel {} already exists'.format(channel_name)

    def __str__(self):
        return self.message


class Broadcaster:
    def __init__(self):
        self.channels = {}

    def send_message(self, message):
        logging.info('Redirecting to: ' + message.channel)
        self.channels[message.channel].send_reply(message)

    def add_channel(self, channel_name, channel_instance):
        self.__add_channel_if_not_exists(channel_name, channel_instance)
        logger.debug('Added channel ' + channel_name)

    def __add_channel_if_not_exists(self, channel_name, channel_instance):
        self.__validate_channel_name(channel_name)
        self.__validate_channel_instance(channel_instance)
        self.channels[channel_name] = channel_instance

    def __validate_channel_name(self, channel_name):
        if channel_name in self.channels:
            raise DuplicateChannelError(channel_name)
        return

    def __validate_channel_instance(self, channel_instance):
        for name, instance in self.channels.items():
            if instance is channel_instance:
                raise DuplicateChannelError(name)
        return
