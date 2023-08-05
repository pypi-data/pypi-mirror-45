import json
from django.http import HttpRequest
from unittest import TestCase

from django_model_builder_service.tests.test_utils import response_json_to_dict
from django_model_builder_service.views import get_model


class TestApi(TestCase):

    def test_get_model_with_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.content_type = 'application/json'
        request.POST = json.loads('{}')
        response = get_model(request)
        response_as_dict = response_json_to_dict(response)
        self.assertEqual(response_as_dict, {'error': 'not a get request'})
