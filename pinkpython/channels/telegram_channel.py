import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from credentials import TELEGRAM_TOKEN
from channels.channel import Channel
from channels.telegram_commands import get_documentation, run_command
from messages.telegram_message import TelegramMessage


logger = logging.getLogger(__name__)


class TelegramChannel(Channel, Updater):
    def __init__(self, inbox_queue):
        Channel.__init__(self, inbox_queue)
        Updater.__init__(self, TELEGRAM_TOKEN)
        self.__load_handlers()
        self.username = 'pinkpythonbot'
        self.username_tag = '@{}'.format(self.username)

    def __load_handlers(self):
        self.__add_mention_receiver()
        self.__add_command('start', self.__start)
        self.__add_command('hello', self.__hello)
        self.__add_command('doc', self.__doc)

    def __add_command(self, label, function):
        command_handler = CommandHandler(label, function)
        self.dispatcher.add_handler(command_handler)

    def __add_mention_receiver(self):
        message_handler = MessageHandler(Filters.text, self.__mention)
        self.dispatcher.add_handler(message_handler)

    def __start(self, bot, update):
        logger.info('[start]: {}'.format(update))
        chat_id = update.message.chat_id
        bot.send_message(chat_id, 'FEED ME')

    def __hello(self, bot, update):
        logger.info('[hello]: {}'.format(update))
        username = self.__get_username_tag(update)
        update.message.reply_text('{} I\'M GONNA EAT U'.format(username))

    def __doc(self, bot, update):
        doc_query = self.__get_message_command('doc', update)
        documentation = get_documentation(doc_query)
        update.message.reply_text(documentation)

    def __run(self, bot, update):
        command = self.__get_message_command('run', update)
        command_output = run_command(command)
        update.message.reply_text(command_output)

    def __get_message_command(self, command, update):
        message = update.message.text.replace('/' + command, '').split()
        message = ' '.join(message)
        return message

    def __get_username_tag(self, update):
        username = update.message.from_user.username
        return '@{}'.format(username)

    def __mention(self, bot, update):
        if self.__is_mention(update):
            message = TelegramMessage(update)
            self.inbox_queue.put(message)

    def __is_mention(self, update):
        if str(update.message.text).startswith(self.username_tag):
            return True
        return False

    def send_reply(self, message):
        original = message.original
        original.reply_text(message.get_reply())

    def init_listener(self):
        logger.debug('Start polling.')
        self.start_polling()
        self.active = True

    def stop_listener(self):
        self.stop()
        self.active = False
