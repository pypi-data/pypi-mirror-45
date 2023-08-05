import os
import sys
import threading

from django_config_initializer_dev.config_initializer_dev import load_config
from prediction_model_wrapper.wrapper.prediction_model_wrapper import PredictionModelWrapper
from swiss_common_utils.utils.log.log_utils import get_logger, log_enter_and_exit

from django_model_prediction_service import views
from django_model_prediction_service.config.config_manager import ConfigManager
from django_model_prediction_service.prediction.prediction_model_handler import PredictionModelHandler
from django_model_prediction_service.views import load_trained_model

logger = get_logger()


def initialize_config_manager():
    views.config_manager = ConfigManager()


def initialize_prediction_model_handler(prediction_model_wrapper):
    views.prediction_model_handler = PredictionModelHandler(prediction_model_wrapper=prediction_model_wrapper,
                                                            config_manager=views.config_manager)


def initialize_load_trained_model_task():
    # Load first model (blocking)
    params = {}
    t = threading.Timer(0.0, load_trained_model, args=[params])
    t.start()
    t.join()

    logger.info('First model loaded? {}'.format(params['result']))


def is_debug():
    return os.environ.get('CONFIG_SERVICE_SETTINGS_DEBUG', 'true').lower() != 'false'


def is_manage_command(command):
    args = sys.argv
    if 'manage.py' in args:
        if command in args:
            logger.info('Running manage.py runserver --> service init')
            return True
        else:
            logger.info('Running some manage.py command other than runserver --> no service init')
            return False

    return False


def should_start_initialize_sequence():
    if is_manage_command('runserver'):
        return True

    if not is_debug():
        logger.info('DEBUG=False --> service init')
        return True

    logger.info('should_start_initialize_sequence returned True')
    return False


# Initialize all tasks here
@log_enter_and_exit
def initialize_service(model_class_fully_qualified_name):
    # migrate & test command may not finish due to the recurring task initialized next.
    # Initialize the recurring task only on runserver command
    if not should_start_initialize_sequence():
        return

    logger.info('Running initializing sequence for service app')

    # Initialization order matters - do not change!
    load_config()
    initialize_config_manager()
    config = views.config_manager.get_config_dict()
    wrapper = PredictionModelWrapper(model_class_fully_qualified_name=model_class_fully_qualified_name, config=config)
    initialize_prediction_model_handler(prediction_model_wrapper=wrapper)

    initialize_load_trained_model_task()
