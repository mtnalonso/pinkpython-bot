import sys
import inspect


class ActionHandler:
    def __init__(self, outbox_queue):
        self.outbox_queue = outbox_queue
        self.__load_actions()

    def __load_actions(self):
        self.actions = {}
        for name, action in self.__find_actions():
            self.actions[name] = action()

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
