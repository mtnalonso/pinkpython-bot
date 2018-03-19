import unittest
import pytest

from nlp.nlp import NLPFactory, NLPResponseError, validate_response
from nlp.dialogflow import DialogflowNLP
from nlp.rasa import RasaNLP


class TestNLPFactory(unittest.TestCase):
    def setUp(self):
        self.factory = NLPFactory

    def test_create_Dialogflow_instance(self):
        dialogflow_instance = self.factory.create('dialogflow')
        assert isinstance(dialogflow_instance, DialogflowNLP)

    def test_create_RasaNLP_instance(self):
        rasa_instance = self.factory.create('rasa')
        assert isinstance(rasa_instance, RasaNLP)

    def test_create_invalid_instance(self):
        with pytest.raises(TypeError):
            instance = self.factory.create('apa')


class TestNLPResponses(unittest.TestCase):
    def setUp(self):
        pass

    def create_http_response(self, status_code):
        response = {'status': {'code': status_code}}
        return response

    def test_valid_http_response(self):
        response = self.create_http_response(200)
        validate_response(response)
        assert True

    def test_server_error_response(self):
        response = self.create_http_response(500)
        with pytest.raises(NLPResponseError):
            validate_response(response)
