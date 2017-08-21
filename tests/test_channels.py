import unittest
import pytest
from queue import Queue

from channels.channel import ChannelSingletonFactory
from channels.twitter_channel import TwitterChannel
from channels.telegram_channel import TelegramChannel


class TestChannelSingletonFactory(unittest.TestCase):
    def setUp(self):
        self.factory = ChannelSingletonFactory()
        self.inbox_queue = Queue()

    def test_create_telegram_channel(self):
        channel = self.factory.get_instance('telegram', self.inbox_queue)
        assert isinstance(channel, TelegramChannel)

    def test_create_twitter_channel(self):
        channel = self.factory.get_instance('twitter', self.inbox_queue)
        assert isinstance(channel, TwitterChannel)

    def test_create_reusing_instances(self):
        first_channel = self.factory.get_instance('telegram',
                                                  self.inbox_queue)
        second_channel = self.factory.get_instance('telegram', None)
        assert second_channel is first_channel

    def test_create_wrong_label(self):
        with pytest.raises(TypeError):
            channel = self.factory.get_instance('twttr', self.inbox_queue)

    def test_create_invalid_queue(self):
        with pytest.raises(TypeError):
            channel = self.factory.get_instance('twitter', None)
