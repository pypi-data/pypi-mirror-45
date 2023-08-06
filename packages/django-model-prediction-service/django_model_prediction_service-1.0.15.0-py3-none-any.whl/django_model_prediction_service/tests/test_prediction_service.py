import json
from unittest import TestCase
from unittest.mock import patch

from django_model_prediction_service.config.config_manager import ConfigManager
from django_model_prediction_service.services.model_loader.handler.prediction_model_handler import \
    PredictionModelHandler
from django_model_prediction_service.services.model_loader.loader.model_builder_service import ModelBuilderService
from django_model_prediction_service.services.model_loader.loader.model_loader import ModelLoader


class TestPredictionService(TestCase):

    @staticmethod
    def mock_get_config_dict():
        return {}

    @patch('django_model_prediction_service.config.config_manager.ConfigManager.get_config_dict',
           new=mock_get_config_dict, create=True)
    def setUp(self):
        config_manager = ConfigManager()
        model_loader = ModelLoader(config_manager=config_manager,
                                   model_builder_service=ModelBuilderService(host='', port=''))
        wrapper = object()

        # Target
        self.prediction_service = PredictionModelHandler(prediction_model_wrapper=wrapper,
                                                         config_manager=config_manager, model_loader=model_loader)

    def test_get_prediction_when_request_missing_job_id(self):
        data_json = json.loads('{}')
        result = self.prediction_service.get_prediction(data_json=data_json)
        self.assertEqual(result, {'error': 'field jobID is missing'})

    def test_get_prediction_when_request_missing_prediction_required_fields(self):
        data_json = json.loads('{"jobID": "test_job_id"}')
        result = self.prediction_service.get_prediction(data_json=data_json)
        self.assertEqual(result, {'error': 'field predictionRequiredFields is missing'})
