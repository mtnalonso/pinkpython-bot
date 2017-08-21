import argparse

from channels.twitter_channel import twitter_channel
import inbox
import outbox


def load_args():
    parser = argparse.ArgumentParser(prog='pinkpython.py')
    parser.add_argument('-c', '--channel', help='Start only given channel')
    return parser.parse_args()


def init_logger():
    import logging
    logging.basicConfig(filename='python_memories.log', filemode='w',
                        level=logging.INFO)


def start_channel(channel):
    if channel == 'twitter':
        start_twitter()


def start_twitter():
    twitter_channel.init_listener()
    start_consumers()


def start_consumers():
    inbox_consumer = inbox.InboxConsumer()
    outbox_consumer = outbox.OutboxConsumer()
    inbox_consumer.start()
    outbox_consumer.start()


def main():
    start_twitter()


if __name__ == '__main__':
    init_logger()

    args = load_args()
    if args.channel:
        start_channel(args.channel)
    else:
        main()
