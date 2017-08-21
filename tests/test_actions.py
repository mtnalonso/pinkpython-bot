import unittest
import pytest
from queue import Queue

from messages.message import Message
from actions.action_handler import ActionHandler
from actions.feed import responses as feed_responses
from actions.greeting import responses as greeting_responses


class TestAction(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()
        self.action = ''
        self.action_handler = ActionHandler(self.queue)
        self.responses = None
        self.valid_responses = None

    def build_message(self, text='', action=None, parameters=None):
        message = Message(text)
        message.action = action or self.action
        message.parameters = parameters
        return message

    def generate_valid_responses(self):
        valid_responses = [r for r in self.responses]
        self.valid_responses = valid_responses

    def get_response_from_queue(self):
        while self.queue.empty():
            pass
        return self.queue.get()


class TestFeedAction(TestAction):
    def setUp(self):
        TestAction.setUp(self)
        self.action = 'feed'
        self.responses = feed_responses

    def generate_valid_responses(self, food):
        valid_responses = [r.format(food) for r in self.responses]
        self.valid_responses = valid_responses

    def test_valid_response(self):
        food = 'mouse'
        message = self.build_message(parameters={'food': [food]})

        self.generate_valid_responses(food)
        self.action_handler.process_message(message)
        response = self.get_response_from_queue()

        assert response.text in self.valid_responses

    def test_invalid_parameter(self):
        message = self.build_message(parameters={'attack': []})

        with pytest.raises(KeyError):
            self.action_handler.process_message(message)

    def test_no_parameters(self):
        message = self.build_message()

        with pytest.raises(TypeError):
            self.action_handler.process_message(message)


class TestGreetingAction(TestAction):
    def setUp(self):
        TestAction.setUp(self)
        self.action = 'greeting'
        self.responses = greeting_responses

    def test_valid_response(self):
        message = self.build_message()

        self.generate_valid_responses()
        self.action_handler.process_message(message)
        response = self.get_response_from_queue()

        assert response.text in self.valid_responses
