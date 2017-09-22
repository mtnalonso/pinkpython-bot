import logging

from channels.channel import Channel
from messages.shell_message import ShellMessage


logger = logging.getLogger(__name__)


class ShellChannel(Channel):
    def __init__(self, inbox_queue):
        Channel.__init__(self, inbox_queue)
        self.inbox_queue = inbox_queue

    def send_reply(self, message):
        print(f'\n-> {message.text}\n')
        self.__request_new_message()

    def init_listener(self):
        self.__request_new_message()

    def stop_listener(self):
        raise SystemExit

    def __request_new_message(self):
        input_message = input('msg> ')
        self.__handle_if_command(input_message)
        message = ShellMessage(input_message)
        self.inbox_queue.put(message)

    def __handle_if_command(self, message):
        if message == '/exit':
            raise SystemExit

