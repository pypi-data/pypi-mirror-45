from swiss_common_utils.sync.mrow_lock.mrow import RWLock
from swiss_logger.log_utils import log_enter_and_exit, print_ascii_art

from django_model_prediction_service import app_globals
from django_model_prediction_service.common.logger import get_logger
from django_model_prediction_service.services.model_loader.loader.model_loader import ModelLoader, model_loader_logger

logger = get_logger()


def generate_exception_error_message(e):
    return 'Exception caught. type: {}, message: {}'.format(type(e), str(e))


def load_trained_model():
    __load_trained_model()


@log_enter_and_exit
def __load_trained_model():
    try:
        load_result = app_globals.prediction_model_handler.load_trained_model()
        model_loader_logger.info('First model loaded? {}'.format(load_result))
    except Exception as e:
        error_msg = generate_exception_error_message(e)
        model_loader_logger.error(error_msg)
        model_loader_logger.error('FAIL TO LOAD MODEL')


class PredictionModelHandler:
    logger = get_logger()
    mrow_lock = RWLock()

    def lock(type):
        def wrap(org_func):
            def wrapped_func(self, *args, **kwargs):
                global logger
                logger.debug('acquiring {} lock'.format(type))

                lock = self.mrow_lock.get_lock(type)

                try:
                    result = org_func(self, *args, **kwargs)
                finally:
                    lock.release()
                    logger.debug('releasing {} lock'.format(type))

                return result

            return wrapped_func

        return wrap

    def __init__(self, prediction_model_wrapper, config_manager, model_loader=None):

        self.config_manager = config_manager

        self.wrapper = prediction_model_wrapper

        if model_loader:
            self.model_loader = model_loader
        else:
            self.model_loader = ModelLoader(config_manager=self.config_manager)

    @lock(type='reader')
    def __get_prediction(self, features_json):
        return self.wrapper.get_prediction(input_features=features_json)

    @lock(type='writer')
    def __set_new_model(self, model_data):
        self.wrapper.load(new_trained_model_data=model_data)

    @staticmethod
    def __generate_result_dict(result=None, error=None, dict_result=None):
        if error:
            result_dict = {'error': error}
        elif dict_result:
            result_dict = dict_result
        else:
            if not result:
                result = ''
            result_dict = {'result': result}
        return result_dict

    def __generate_prediction_result(self, job_id, prediction_result):
        prediction_result = {
            'jobID': job_id,
            'jobPredictionResult': {
                'result': prediction_result
            },
            'classifierID': self.model_loader.get_model_identifier()
        }
        return prediction_result

    def get_prediction(self, data_json):
        global logger
        if not self.wrapper:
            msg = 'model not loaded'
            logger.error(msg)
            return self.__generate_result_dict(error=msg)

        if 'jobID' not in data_json:
            return self.__generate_result_dict(error='field jobID is missing')
        job_id = data_json['jobID']

        pool_name = ''
        if 'poolName' in data_json:
            pool_name = data_json['poolName']

        if 'predictionRequiredFields' not in data_json:
            return self.__generate_result_dict(error='field predictionRequiredFields is missing')
        features_json = data_json['predictionRequiredFields']

        logger.info('Job ID: {}'.format(job_id))
        logger.info('Pool name: {}'.format(pool_name))
        logger.info('features: {}'.format(features_json))

        prediction_result = self.__get_prediction(features_json)
        prediction_result = self.__generate_prediction_result(job_id=job_id, prediction_result=prediction_result)
        logger.info('prediction: {}'.format(prediction_result))
        return prediction_result

    def load_trained_model(self):
        print_ascii_art('LOAD MODEL')
        model_data = self.model_loader.get_model()
        self.__set_new_model(model_data=model_data)
        return True
