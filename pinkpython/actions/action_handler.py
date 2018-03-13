import sys
import inspect
import logging
from importlib import import_module
from os import listdir
from os.path import isfile, join, splitext, dirname, abspath

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
        for name, action in self.__find_actions():
            self.actions[name] = action()

    def __find_actions(self):
        for action_filename in self.__get_actions_filenames():
            module = import_module('actions.' + action_filename)
            class_ = getattr(module, dir(module)[1])
            yield action_filename, class_

    def __get_actions_filenames(self):
        path = dirname(abspath(__file__))
        files = [splitext(f)[0] for f in listdir(path) if isfile(join(path,f))]
        files = self.__filter_action_files(files)
        return files

    def __filter_action_files(self, found_files):
        files_to_remove = ['__init__', 'action', 'action_handler']
        filtered_files = [f for f in found_files if f not in files_to_remove]
        filtered_files = [f for f in filtered_files if f[0] not in ['.', '_']]

        logger.info('filtered files {}'.format(filtered_files))
        return filtered_files

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
