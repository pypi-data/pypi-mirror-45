import base64
import json
import requests
from swiss_common_utils.utils.log.log_utils import get_logger

from django_model_prediction_service.prediction.exceptions.ModelSourceNotConfiguredError import ModelSourceNotConfigured
from django_model_prediction_service.prediction.model.model_builder_service import ModelBuilderService


class ModelLoader:
    logger = get_logger()

    MODEL_SOURCE_PATH = 'model_source_path'
    MODEL_LOAD_BUILDER_SERVICE_URL = 'model_source_builder_service_url'
    MODEL_LOAD_BUILDER_SERVICE_PORT = 'model_source_builder_service_port'

    def __init__(self, config_manager, model_builder_service=None):
        self.config_manager = config_manager
        self.model_identifier = ''
        self.model_build_time = ''
        self.model = None

        if model_builder_service:
            self.model_builder_service = model_builder_service
        else:
            self.model_builder_service = ModelBuilderService(host='', port='')

    def __can_load_model_from_filesystem(self):
        return self.config_manager.is_config_key_exists(self.MODEL_SOURCE_PATH)

    def __can_load_model_from_remote_service(self):
        return self.config_manager.is_config_key_exists(
            self.MODEL_LOAD_BUILDER_SERVICE_URL)

    def __decode_model(self, model_data):
        model = model_data.encode()

        model_dec = base64.b64decode(model)
        return model_dec

    def __load_model_from_filesystem(self, src):
        src = self.config_manager.get_config_val(self.MODEL_SOURCE_PATH)
        self.logger.info('Loading trained prediction from: {}'.format(src))

        f_model = open(src, 'r')
        model_data = f_model.read()
        return json.loads(model_data)

    def __is_http_code_ok(self, response_code):
        self.logger.info('HTTP response code: ' + str(response_code))
        if response_code != 200:
            self.logger.error('HTTP response code description: ' + requests.status_codes._codes[response_code][0])

    def __load_model_from_remote_service(self):
        host = self.config_manager.get_config_val_with_default(self.MODEL_LOAD_BUILDER_SERVICE_URL, default='')
        port = self.config_manager.get_config_val_with_default(self.MODEL_LOAD_BUILDER_SERVICE_PORT, default='')
        self.model_builder_service.host = host
        self.model_builder_service.port = port
        return self.model_builder_service.get_model()

    def get_model_identifier(self):
        return self.model_identifier

    def get_model_build_time(self):
        return self.model_build_time

    def get_model(self):
        if self.__can_load_model_from_filesystem():
            src = self.config_manager.get_config_val(self.MODEL_SOURCE_PATH)
            model_data = self.__load_model_from_filesystem(src=src)
        elif self.__can_load_model_from_remote_service():
            model_data = self.__load_model_from_remote_service()
        else:
            msg = 'model source not configured'
            self.logger.error(msg)
            raise ModelSourceNotConfigured(msg)

        self.model_identifier = model_data['identifier']
        self.model_build_time = model_data['build_time']

        self.logger.info('model identifier: {}'.format(self.model_identifier))
        self.logger.info('model build time: {}'.format(self.model_build_time))
        self.logger.info('Size of model data: {} KB'.format(int(len(str(model_data).encode('utf-8')) / 1024)))

        model_data_encoded = model_data['model']
        self.model = self.__decode_model(model_data_encoded)
        model_data['model'] = self.model

        return model_data
