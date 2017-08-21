import logging
from telegram.ext import Updater, CommandHandler

from credentials import TELEGRAM_TOKEN
from channels.channel import Channel


logger = logging.getLogger(__name__)


class TelegramChannel(Channel):
    def __init__(self, inbox_queue):
        Channel.__init__(self, inbox_queue)

    def send_message(self, message):
        print(message)

    def send_reply(self, message):
        print(message)

    def init_listener(self):
        logger.debug('Start listening...')
