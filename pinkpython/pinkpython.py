from channels.twitter import twitter_channel
import inbox
import outbox


def start_consumers():
    inbox_consumer = inbox.InboxConsumer()
    outbox_consumer = outbox.OutboxConsumer()
    inbox_consumer.start()
    outbox_consumer.start()

def main():
    twitter_channel.init_listener()
    start_consumers()


if __name__ == '__main__':
    main()
