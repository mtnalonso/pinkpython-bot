from abc import ABC, abstractmethod
import json
from configparser import ConfigParser
from pprint import pprint
import requests
import apiai

from model.message import Message


class NLPResponseError(Exception):
    def __init__(self, message):
        Exception.__init__(message)


class NLP(ABC):
    def __init__(self, language='en', session_id='pink'):
        self.language = language
        self.session_id = session_id

    def process(self, message):
        response = self.send_request(message.text)
        self.validate_response(response)
        message = self.add_nlp_data(response, message)
        return message

    def add_nlp_data(self, response, message):
        result = response['result']
        message.action = self.get_action(result)
        message.parameters = result['parameters']
        message.query = result['resolvedQuery']
        return message

    def validate_response(self, response):
        if response['status']['code'] != 200:
            raise NLPResponseError('status code ' +
                                   response['status']['code'])

    @abstractmethod
    def send_request(self, message):
        pass

    @abstractmethod
    def get_action(self, response):
        pass


class APINLP(NLP):
    def __init__(self):
        super(APINLP, self).__init__()
        from credentials import apiai_access_token_developer
        self.ai = apiai.ApiAI(apiai_access_token_developer)

    def send_request(self, message):
        request = self.build_request(message)
        response = request.getresponse()
        return json.loads(response.read().decode('utf-8'))

    def get_action(self, result):
        return result['action']

    def build_request(self, message):
        request = self.ai.text_request()
        request.query = message
        request.lang = self.language
        request.session_id = self.session_id
        return request

class RasaNLP(NLP):
    def __init__(self):
        super(RasaNLP, self).__init__()
        config = ConfigParser()
        config.read('pinkpython.conf')
        self.host = config.get('nlp', 'rasa_host')
        self.port = config.get('nlp', 'rasa_port')
        self.url = self.build_url()

    def send_request(self, message):
        http_response = requests.get(self.url + message)
        return json.loads(http_response.text)

    def get_action(self, result):
        return result['metadata']['intentName']['name']

    def build_url(self):
        return str('http://' + self.host + ':' + self.port + '/parse?q=')


class NLPFactory:
    config = ConfigParser()
    config.read('pinkpython.conf')
    CLASSES = {
        'api': APINLP,
        'rasa': RasaNLP
    }

    @staticmethod
    def create():
        nlp_label = NLPFactory.config.get('nlp', 'nlp')
        nlp = NLPFactory.CLASSES.get(nlp_label)
        return nlp()
