import logging


logger = logging.getLogger(__name__)


class Broadcaster:
    def __init__(self):
        self.channels = {}

    def send_message(self, message):
        logging.info('Redirecting to: ' + message.channel)
        self.channels[message.channel].send_reply(message)

    def add_channel(self, channel_name, channel_instance):
        self.channels[channel_name] = channel_instance
        logger.info('Added channel ' + channel_name)
