import json
from unittest import TestCase

from django.http import HttpRequest

from django_model_prediction_service.tests.test_utils import response_json_to_dict
from django_model_prediction_service.views import get_prediction


class TestApi(TestCase):

    def test_get_prediction_with_get_method(self):
        request = HttpRequest()
        request.method = 'GET'
        response = get_prediction(request)
        response_as_dict = response_json_to_dict(response)
        self.assertEqual(response_as_dict, {'error': 'not a post request'})

    def test_get_prediction_with_invalid_content_type(self):
        request = HttpRequest()
        request.method = 'POST'
        request.content_type = 'text/plain'
        request.POST = json.loads('{}')
        response = get_prediction(request)
        response_as_dict = response_json_to_dict(response)
        self.assertEqual(response_as_dict, {'error': 'invalid request content type'})
