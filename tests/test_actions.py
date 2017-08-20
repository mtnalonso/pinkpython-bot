import unittest
from queue import Queue

from messages.message import Message
from actions.action_handler import ActionHandler
from actions.feed import responses as feed_responses


class TestFeedAction(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()
        self.action_handler = ActionHandler(self.queue)
        self.responses = feed_responses

    def test_valid_response(self):
        message = Message('')
        message.action = 'feed'
        food = 'mouse'
        message.parameters = {'food': [food]}

        valid_responses = [x.format(food) for x in self.responses]

        self.action_handler.process_message(message)
        while self.queue.empty():
            pass

        output_message = self.queue.get()
        response = output_message.text

        assert response in valid_responses


if __name__ == '__main__':
    unittest.main()
