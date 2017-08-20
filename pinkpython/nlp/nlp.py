from abc import ABC, abstractmethod
import config


class NLPResponseError(Exception):
    def __init__(self, message):
        Exception.__init__(message)


def validate_response(self, response):
    if response['status']['code'] != 200:
        raise NLPResponseError('status code ' + response['status']['code'])


class NLP(ABC):
    def __init__(self, language='en', session_id='pink'):
        self.language = language
        self.session_id = session_id

    def process(self, message):
        response = self.send_request(message.text)
        validate_response(response)
        message = self.add_nlp_data(response, message)
        return message

    def add_nlp_data(self, response, message):
        result = response['result']
        message.action = self.get_action(result)
        message.parameters = result['parameters']
        message.query = result['resolvedQuery']
        return message

    @abstractmethod
    def send_request(self, message):
        pass

    @abstractmethod
    def get_action(self, response):
        pass


class NLPFactory:
    from nlp.rasa import RasaNLP
    from nlp.api import APINLP

    CLASSES = {
        'api': APINLP,
        'rasa': RasaNLP
    }

    @staticmethod
    def create():
        nlp_label = config.NLP
        nlp = NLPFactory.CLASSES.get(nlp_label)
        return nlp()
