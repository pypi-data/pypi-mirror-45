import os
import sys
import threading

from swiss_common_utils.utils.log.log_utils import get_logger, log_enter_and_exit
from swiss_common_utils.utils.yml.yaml_utils import yaml_to_flat_dict

from django_model_prediction_service.config.config_manager import ConfigManager
from django_model_prediction_service.prediction.prediction_model_handler import PredictionModelHandler
from django_model_prediction_service.views import load_trained_model

logger = get_logger()


@log_enter_and_exit
def initialize_environment_variables_for_dev_environment():
    logger.info('[ENTER] initialize_environment_variables_for_dev_environment')
    if not should_start_initialize_sequence():
        return

    config_path = 'service/config/config_dev.yml'
    var_dict = yaml_to_flat_dict(src_file=config_path)
    for k, v in var_dict.items():
        key = '_'.join(['CONFIG_SERVICE', k.upper()])
        logger.debug('setting environment variable: {}={}'.format(key, v))
        os.environ[key] = str(v)


def initialize_config_manager():
    views.config_manager = ConfigManager()


def initialize_prediction_model_handler():
    views.prediction_model_handler = PredictionModelHandler(config_manager=views.config_manager)


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
def initializae_background_tasks():
    # migrate & test command may not finish due to the recurring task initialized next.
    # Initialize the recurring task only on runserver command
    if not should_start_initialize_sequence():
        return

    logger.info('Running initializing sequence for service app')

    # Initialization order matters - do not change!
    initialize_config_manager()
    initialize_prediction_model_handler()

    initialize_load_trained_model_task()
