import argparse
from queue import Queue

from channels.channel import ChannelFactory, TWITTER, TELEGRAM
from channels.broadcaster import Broadcaster
from inbox import InboxConsumer
from outbox import OutboxConsumer


def init_logger():
    import logging
    logging.basicConfig(filename='python_memories.log', filemode='w',
                        level=logging.INFO)


def load_args():
    parser = argparse.ArgumentParser(prog='pinkpython.py')
    parser.add_argument('-c', '--channel', help='Start only given channel')
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
    init_logger()

    args = load_args()
    main(args.channel)
