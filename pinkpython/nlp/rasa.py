import json
import requests
from nlp.nlp import NLP


class RasaNLP(NLP):
    def __init__(self):
        super(RasaNLP, self).__init__()
        config = ConfigParser()
        config.read('configuration.conf')
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
