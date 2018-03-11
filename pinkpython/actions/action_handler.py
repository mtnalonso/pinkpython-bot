import sys
import inspect
import logging

from actions.feed import Feed
from actions.greeting import Greeting
from actions.error import Error
from actions.dummy import Dummy


logger = logging.getLogger(__name__)


class ActionHandler:
    def __init__(self, outbox_queue):
        self.outbox_queue = outbox_queue
        self.actions = {}
        self.__load_actions()

    def __load_actions(self):
        logger.info('Loading actions')
        self.actions['dummy'] = Dummy()
        self.actions['error'] = Error()
        self.actions['feed'] = Feed()
        self.actions['greeting'] = Greeting()
        #for name, action in self.__find_actions():
        #    self.actions[name] = action()

    def __find_actions(self):
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj) and __name__ != obj.__module__:
                yield name.lower(), obj

    def process_message(self, message):
        params = message.parameters
        intent = message.action
        message.text = self.__start_action(intent, params)
        self.__send_message(message)

    def __start_action(self, intent, params):
        current_action = self.__get_action(intent)
        current_action.execute(params)
        response = current_action.get_response_message()
        return response

    def __get_action(self, intent):
        try:
            action = self.actions[intent]
        except KeyError:
            action = self.__get_error_action()
        return action

    def __get_error_action(self):
        return self.actions.get('error')

    def __send_message(self, message):
        self.outbox_queue.put(message)
