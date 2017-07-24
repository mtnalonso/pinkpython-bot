from abc import ABC, abstractmethod
import json
from configparser import ConfigParser
import requests
import apiai


class NLPResponse:
    def __init__(self, action, query='', parameters={}, language='en'):
        self.action = action
        self.query = query
        self.parameters = parameters
        self.language = language
        self.generated_response = None
        self.platform = None

    def __repr__(self):
        return ('action:\t' + str(self.action) + '\nquery:\t' +
                str(self.query) + '\nparams:\t' + str(self.parameters))


class NLPResponseError(Exception):
    def __init__(self, message):
        Exception.__init__(message)


class NLP(ABC):
    def __init__(self, language='en', session_id='pink'):
        self.language = language
        self.session_id = session_id

    def process(self, message):
        response = self.send_request(message)
        self.validate_response(response)
        response = self.process_response(response)
        return response

    @abstractmethod
    def send_request(self, message):
        pass

    @abstractmethod
    def validate_response(self, response):
        pass

    @abstractmethod
    def process_response(self, response):
        pass

    def validate_response(self, response):
        if response['status']['code'] != 200:
            raise NLPResponseError('status code ' +
                                   response['status']['code'])

class APINLP(NLP):
    def __init__(self):
        super(APINLP, self).__init__()
        from credentials import apiai_access_token_developer
        self.ai = apiai.ApiAI(apiai_access_token_developer)

    def send_request(self, message):
        request = self.build_request(message)
        response = request.getresponse()
        return json.loads(response.read().decode('utf-8'))

    def process_response(self, response):
        result = response['result']
        parameters = result['parameters']
        action = result['action']
        query = result['resolvedQuery']
        response = NLPResponse(action, query=query, parameters=parameters)
        response.generated_response = result['fulfillment']['speech']
        return response

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
        self.url = self.build_url

    def send_request(self, message):
        http_response = requests.get(self.url + message)
        return json.loads(http_response.text)

    def process_response(self, response):
        result = response['result']
        parameters = result['parameters']
        action = result['metadata']['intentName']['name']
        query = result['resolvedQuery']
        response = NLPResponse(action, query=query, parameters=parameters)
        response.generated_response = 'THIS IS A RASA TEST'
        return response

    def build_url(self):
        return ('http://' + self.host + ':' + self.port + '/parse?q=')


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
