from abc import ABC, abstractmethod
import json
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
        """
        handle configuration
        """
        self.language = language
        self.session_id = session_id

    @abstractmethod
    def process(self, message):
        pass


class APINLP(NLP):
    def __init__(self):
        super(APINLP, self).__init__()
        from credentials import apiai_access_token_developer
        self.ai = apiai.ApiAI(apiai_access_token_developer)

    def process(self, message):
        ai_response = self.send_request(message)
        self.validate_response(ai_response)
        response = self.process_nlp_response(ai_response)
        return response

    def send_request(self, message):
        request = self.build_request()
        request.query = message
        response = request.getresponse()
        return json.loads(response.read().decode('utf-8'))

    def build_request(self):
        request = self.ai.text_request()
        request.lang = self.language
        request.session_id = self.session_id
        return request

    def process_nlp_response(self, ai_response):
        result = ai_response['result']
        parameters = result['parameters']
        action = result['action']
        query = result['resolvedQuery']
        response = NLPResponse(action, query=query, parameters=parameters)
        response.generated_response = result['fulfillment']['speech']
        return response

    def validate_response(self, ai_response):
        if ai_response['status']['code'] != 200:
            raise NLPResponseError('status code ' +
                                   ai_response['status']['code'])


class RasaNLP(NLP):
    def __init__(self):
        super(RasaNLP, self).__init__()
        raise NotImplementedError

    def process(self, message):
        raise NotImplementedError


class NLPFactory:
    CLASSES = {
        'api': APINLP,
        'rasa': RasaNLP
    }

    @staticmethod
    def create():
        # apply configuration
        #nlp = config.get('nlp')
        nlp = 'api'
        clazz = NLPFactory.CLASSES.get(nlp)
        return clazz()
