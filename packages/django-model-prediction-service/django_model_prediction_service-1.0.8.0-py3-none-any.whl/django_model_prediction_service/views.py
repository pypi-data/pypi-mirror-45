import json
import threading
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from swiss_common_utils.utils.datetime.datetime_utils import time_string_to_seconds
from swiss_common_utils.utils.log.log_utils import get_logger, log_enter_and_exit

logger = get_logger()

prediction_model_handler = None
config_manager = None


def generate_error_json_response(error):
    return JsonResponse({"error": error})


def generate_exception_error_message(e):
    return 'Exception caught. type: {}, message: {}'.format(type(e), str(e))


@csrf_exempt  # TODO: this disables csrf protection, should find a different solution
def get_prediction(request):
    if request.method != 'POST':
        return generate_error_json_response('not a post request')
    if request.content_type != 'application/json':
        return generate_error_json_response('invalid request content type')
    try:
        data = request.body.decode('utf-8')
        data_json_obj = json.loads(data)
        global prediction_model_handler
        prediction_result = prediction_model_handler.get_prediction(data_json_obj)
        return JsonResponse(prediction_result)
    except Exception as e:
        error_msg = generate_exception_error_message(e)
        logger.error(error_msg)
        return generate_error_json_response(error_msg)


@log_enter_and_exit
def load_trained_model(params):
    try:
        temp_params = {}
        global config_manager
        load_interval_str = config_manager.get_config_val_with_default('model_load_interval', default='6h')
        logger.info('Model load interval: {}'.format(load_interval_str))
        load_interval_seconds = time_string_to_seconds(load_interval_str)
        if load_interval_seconds > 10.0:
            t = threading.Timer(function=load_trained_model, args=[temp_params], interval=load_interval_seconds)
            t.start()

        global prediction_model_handler
        params['result'] = prediction_model_handler.load_trained_model()

    except Exception as e:
        error_msg = generate_exception_error_message(e)
        logger.error(error_msg)
        logger.error('FAIL TO LOAD MODEL')
        params['result'] = error_msg
