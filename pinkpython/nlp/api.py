import json
import apiai
from nlp.nlp import NLP


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
        return result['action']

    def build_request(self, message):
        request = self.apiai.text_request()
        request.query = message
        request.lang = self.language
        request.session_id = self.session_id
        return request
