import unittest
import pytest
from queue import Queue

from channels.channel import ChannelFactory
from channels.twitter_channel import TwitterChannel
from channels.telegram_channel import TelegramChannel


class TestChannelFactory(unittest.TestCase):
    def setUp(self):
        self.factory = ChannelFactory
        self.inbox_queue = Queue()

    def test_create_telegram_channel(self):
        channel = self.factory.create('telegram', self.inbox_queue)
        assert isinstance(channel, TelegramChannel)

    def test_create_twitter_channel(self):
        channel = self.factory.create('twitter', self.inbox_queue)
        assert isinstance(channel, TwitterChannel)

    def test_create_wrong_label(self):
        with pytest.raises(TypeError):
            channel = self.factory.create('twttr', self.inbox_queue)

    def test_create_invalid_queue(self):
        with pytest.raises(TypeError):
            channel = self.factory.create('twitter', None)
