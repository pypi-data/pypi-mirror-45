from unittest import TestCase
from unittest.mock import patch

from django_model_prediction_service.config.config_manager import ConfigManager
from django_model_prediction_service.prediction.model.model_builder_service import ModelBuilderService
from django_model_prediction_service.prediction.model.model_loader import ModelLoader


class TestModelLoader(TestCase):

    def setUp(self):
        # Target
        self.model_loader = ModelLoader(config_manager=ConfigManager(),
                                        model_builder_service=ModelBuilderService('', ''))

    @patch.object(ConfigManager, 'is_config_key_exists')
    @patch.object(ModelBuilderService, 'get_model')
    def test_get_model(self, mock_get_model, mock_is_config_key_exists):
        expected_result_dict = {
            'model': 'dGVzdF9tb2RlbA==',
            'identifier': 'test_identifier',
            'build_time': 'test_build_time'
        }

        def is_config_key_exists_side_effect(key):
            if key == 'model_source_builder_service_url' or key == 'model_source_builder_service_port':
                return 'not empty'
            return ''

        mock_is_config_key_exists.side_effect = is_config_key_exists_side_effect

        mock_get_model.return_value = expected_result_dict

        model_data = self.model_loader.get_model()
        model = model_data['model'].decode()
        self.assertEqual(model, 'test_model')

        model_identifier = self.model_loader.get_model_identifier()
        self.assertEqual(model_identifier, 'test_identifier')

        build_time = self.model_loader.get_model_build_time()
        self.assertEqual(build_time, 'test_build_time')



