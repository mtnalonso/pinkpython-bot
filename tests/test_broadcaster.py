import unittest
import pytest
from queue import Queue

from channels.broadcaster import Broadcaster, DuplicateChannelError
from channels.channel import ChannelFactory, TWITTER, TELEGRAM


class TestBroadcaster(unittest.TestCase):
    def setUp(self):
        self.broadcaster = Broadcaster()
        self.factory = ChannelFactory
        self.inbox_queue = Queue()

    def test_add_channel(self):
        channel = self.factory.create(TWITTER, self.inbox_queue)
        self.broadcaster.add_channel(TWITTER, channel)

        assert TWITTER in self.broadcaster.channels
        assert channel is self.broadcaster.channels[TWITTER]

    def test_add_duplicate_channel_label(self):
        channel_one = self.factory.create(TWITTER, self.inbox_queue)
        channel_two = self.factory.create(TWITTER, self.inbox_queue)

        self.broadcaster.add_channel(TWITTER, channel_one)

        with pytest.raises(DuplicateChannelError):
            self.broadcaster.add_channel(TWITTER, channel_two)

    def test_add_duplicate_channel_instance(self):
        channel = self.factory.create(TWITTER, self.inbox_queue)

        self.broadcaster.add_channel(TWITTER, channel)

        with pytest.raises(DuplicateChannelError):
            self.broadcaster.add_channel(TWITTER, channel)

    @unittest.skip('Checkout threads')
    def test_stop_channels(self):
        channel_one = self.__start_channel(TELEGRAM)
        channel_two = self.__start_channel(TWITTER)

        self.broadcaster.stop_channels()

        assert channel_one.active is False
        assert channel_two.active is False

    def __start_channel(self, channel_name):
        channel = self.factory.create(channel_name, self.inbox_queue)
        self.broadcaster.add_channel(channel_name, channel)
        channel.init_listener()
        return channel
