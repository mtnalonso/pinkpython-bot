from channels.twitter import twitter_channel
import inbox
import outbox


def init_logger():
    import logging
    logging.basicConfig(filename='python_memories.log', filemode='w',
                        level=logging.INFO)

def start_consumers():
    inbox_consumer = inbox.InboxConsumer()
    outbox_consumer = outbox.OutboxConsumer()
    inbox_consumer.start()
    outbox_consumer.start()

def main():
    twitter_channel.init_listener()
    start_consumers()


if __name__ == '__main__':
    init_logger()
    main()
