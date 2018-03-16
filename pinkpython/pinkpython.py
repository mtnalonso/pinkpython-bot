import argparse
import logging
import logging.handlers
from logging.config import dictConfig
from queue import Queue

from channels.channel import ChannelFactory, TWITTER, TELEGRAM
from channels.broadcaster import Broadcaster
from inbox import InboxConsumer
from outbox import OutboxConsumer


logger = logging.getLogger(__name__)

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
}


def init_logger(debug):
    dictConfig(DEFAULT_LOGGING)
    formatter = logging.Formatter(
            '%(asctime)s - %(levelname)-8s %(name)-12s: %(message)s')
    logging.root.setLevel(logging.DEBUG)

    if debug:
        activate_stream_logging(formatter)
    activate_file_logging(formatter)


def activate_file_logging(formatter):
    file_handler = logging.FileHandler('python_memories.log',
                                       mode='w', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logging.root.addHandler(file_handler)


def activate_stream_logging(formatter):
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logging.root.addHandler(console_handler)


def load_args():
    parser = argparse.ArgumentParser(prog='pinkpython.py')
    parser.add_argument('-c', '--channel', help='Start only given channel')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Show debugging information on shell')
    return parser.parse_args()


def main(channel):
    inbox_queue = Queue()
    outbox_queue = Queue()
    broadcaster = Broadcaster()

    if channel:
        start_channel(channel, inbox_queue, broadcaster)
    else:
        start_all(inbox_queue, broadcaster)
    start_consumers(inbox_queue, outbox_queue, broadcaster)


def start_all(inbox_queue, broadcaster):
    ''' Shell channel omitted here '''
    start_channel(TELEGRAM, inbox_queue, broadcaster)
    start_channel(TWITTER, inbox_queue, broadcaster)


def start_channel(channel_name, inbox_queue, broadcaster):
    channel = ChannelFactory.create(channel_name, inbox_queue)
    broadcaster.add_channel(channel_name, channel)
    channel.init_listener()


def start_consumers(inbox_queue, outbox_queue, broadcaster):
    inbox_consumer = InboxConsumer(inbox_queue, outbox_queue)
    outbox_consumer = OutboxConsumer(outbox_queue, broadcaster)
    inbox_consumer.start()
    outbox_consumer.start()


if __name__ == '__main__':
    args = load_args()
    init_logger(args.debug)
    main(args.channel)
