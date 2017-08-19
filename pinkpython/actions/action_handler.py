from actions.feed import Feed
from actions.action_test import Test
from actions.error import Error
from actions.greeting import Greeting
import outbox


class ActionHandler:
    def __init__(self, outbox_queue=outbox.outbox_queue):
        self.actions = self.__load_actions()
        self.outbox_queue = outbox_queue

    def __load_actions(self):
        actions = {}
        actions['feed'] = Feed()
        actions['test'] = Test()
        actions['greeting'] = Greeting()
        return actions

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
        return Error()

    def __send_message(self, message):
        self.outbox_queue.put(message)
