import json
import apiai
import requests
from nlp.nlp import NLP


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
