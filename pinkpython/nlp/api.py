import json
import logging

import apiai

from nlp.nlp import NLP


logger = logging.getLogger(__name__)


class APINLP(NLP):
    def __init__(self):
        super(APINLP, self).__init__()
        from credentials import APIAI_ACCESS_TOKEN_DEVELOPER
        self.apiai = apiai.ApiAI(APIAI_ACCESS_TOKEN_DEVELOPER)

    def send_request(self, message):
        request = self.build_request(message)
        response = request.getresponse()
        return json.loads(response.read().decode('utf-8'))

    def get_action(self, result):
        try:
            return result['action']
        except KeyError:
            logging.error['There is no action defined for this action']
            return 'error'

    def build_request(self, message):
        request = self.apiai.text_request()
        request.query = message
        request.lang = self.language
        request.session_id = self.session_id
        return request
