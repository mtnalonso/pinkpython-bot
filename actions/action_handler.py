from model.message import Message
from outbox import Outbox
from actions.feed import Feed
from actions.action_test import Test


outbox = Outbox()


class ActionHandler:
    def __init__(self, outbox=outbox):
        self.actions = self.__load_actions()
        self.outbox = outbox
        self.outbox.start()

    def __load_actions(self):
        actions = {}
        actions['feed'] = Feed()
        actions['test'] = Test()
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
        return self.actions[intent]

    def __send_message(self, message):
        self.outbox.put_message(message)
