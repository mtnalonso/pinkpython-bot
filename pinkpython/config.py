from os.path import abspath, dirname, join
from configparser import ConfigParser


project_root_path = abspath(join(dirname(__file__), '..'))


config = ConfigParser()
config.read(project_root_path + '/configuration.conf')


twitter_username = config.get('twitter', 'username')


nlp = config.get('nlp', 'nlp')

try:
    rasa_port = config.get('nlp', 'rasa_port')
    rasa_host = config.get('nlp', 'rasa_host')
except ConfigParser.NoOptionError:
    pass
