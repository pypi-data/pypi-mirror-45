from datetime import datetime

from swiss_common_utils.utils.datetime.datetime_utils import datetime_to_millis
from swiss_common_utils.utils.log.log_utils import get_logger, print_ascii_art

from django_model_prediction_service.prediction.model.model_loader import ModelLoader
from django_model_prediction_service.prediction.mrow_lock.mrow import RWLock


class PredictionModelHandler:
    logger = get_logger()
    mrow_lock = RWLock()

    def lock(type):
        def wrap(org_func):
            def wrapped_func(self, *args, **kwargs):
                self.logger.debug('acquiring {} lock'.format(type))

                if type == 'writer':
                    lock = self.mrow_lock.writer()
                else:
                    lock = self.mrow_lock.reader()

                result = org_func(self, *args, **kwargs)

                lock.release()
                self.logger.debug('releasing {} lock'.format(type))

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
        self.wrapper.load(data=model_data)

    def __generate_result_dict(self, result=None, error=None, dict_result=None):
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
            'classifierID': datetime_to_millis(
                datetime.strptime(self.model_loader.get_model_build_time(), '%Y-%m-%d %H:%M:%S.%f'))
        }
        return prediction_result

    def get_prediction(self, data_json):
        if not self.wrapper:
            msg = 'model not loaded'
            self.logger.error(msg)
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

        self.logger.info('Job ID: {}'.format(job_id))
        self.logger.info('Pool name: {}'.format(pool_name))
        self.logger.info('features: {}'.format(features_json))

        prediction_result = self.__get_prediction(features_json)
        prediction_result = self.__generate_prediction_result(job_id=job_id, prediction_result=prediction_result)
        self.logger.info('prediction: {}'.format(prediction_result))
        return prediction_result

    def load_trained_model(self):
        print_ascii_art('LOAD MODEL')
        model_data = self.model_loader.get_model()
        self.__set_new_model(model_data=model_data)
        return True
