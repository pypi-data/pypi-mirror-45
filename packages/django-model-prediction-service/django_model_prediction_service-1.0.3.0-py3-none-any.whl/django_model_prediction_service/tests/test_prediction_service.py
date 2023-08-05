import json
from unittest import TestCase
from unittest.mock import patch

from django_model_prediction_service.config.config_manager import ConfigManager
from django_model_prediction_service.prediction.model.model_builder_service import ModelBuilderService
from django_model_prediction_service.prediction.model.model_loader import ModelLoader
from django_model_prediction_service.prediction.prediction_model_handler import PredictionModelHandler


class TestPredictionService(TestCase):

    @staticmethod
    def mock_get_config_dict():
        return {}

    @patch('service.config.config_manager.ConfigManager.get_config_dict', new=mock_get_config_dict, create=True)
    def setUp(self):
        config_manager = ConfigManager()
        model_loader = ModelLoader(config_manager=config_manager, model_builder_service=ModelBuilderService(host='', port=''))

        # Target
        self.prediction_service = PredictionModelHandler(config_manager=config_manager, model_loader=model_loader)

    def test_get_prediction_when_request_missing_job_id(self):
        data_json = json.loads('{}')
        result = self.prediction_service.get_prediction(data_json=data_json)
        self.assertEqual(result, {'error': 'field jobID is missing'})

    def test_get_prediction_when_request_missing_prediction_required_fields(self):
        data_json = json.loads('{"jobID": "test_job_id"}')
        result = self.prediction_service.get_prediction(data_json=data_json)
        self.assertEqual(result, {'error': 'field predictionRequiredFields is missing'})
