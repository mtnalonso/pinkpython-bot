import unittest
import pytest
from random import choice

from nlp.nlp import NLPFactory
from messages.message import Message


foods = [
    'mouse', 'meat', 'rat', 'bird'
]


class TestIntentFeed(unittest.TestCase):
    def setUp(self):
        self.nlp = NLPFactory.create()
        self.expected_action = 'feed'
        self.food = None

    def create_message(self):
        self.food = choice(foods)
        message = Message('Here\'s a {0} for u'.format(self.food))
        return message

    @unittest.skip('Depends on AI data')
    def test_feed_intent_valid(self):
        message = self.create_message()

        response = self.nlp.process(message)
        parameters = response.parameters

        assert response.action == self.expected_action
        assert self.food == parameters['food'][0]
