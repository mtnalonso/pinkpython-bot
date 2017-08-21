import unittest
import pytest
from queue import Queue

from channels.channel import ChannelFactory
from channels.twitter_channel import TwitterChannel
from channels.telegram_channel import TelegramChannel


class TestChannelFactory(unittest.TestCase):
    def setUp(self):
        self.factory = ChannelFactory()
        self.inbox_queue = Queue()

    def test_create_telegram_channel(self):
        channel = self.factory.create('telegram', self.inbox_queue)
        assert isinstance(channel, TelegramChannel)
