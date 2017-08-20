from os.path import abspath, dirname, join
from configparser import ConfigParser, NoOptionError
import logging


logger = logging.getLogger(__name__)


PROJECT_ROOT_PATH = abspath(join(dirname(__file__), '..'))


config = ConfigParser()
config.read(PROJECT_ROOT_PATH + '/configuration.conf')


TWITTER_USERNAME = config.get('twitter', 'username')


NLP = config.get('nlp', 'nlp')

try:
    RASA_PORT = config.get('nlp', 'rasa_port')
    RASA_HOST = config.get('nlp', 'rasa_host')
except NoOptionError as error:
    logger.error(str(error))
