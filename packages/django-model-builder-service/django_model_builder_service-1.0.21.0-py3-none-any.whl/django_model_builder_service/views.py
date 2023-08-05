import json
import threading

import pytz
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from swiss_common_utils.utils.datetime.datetime_utils import time_string_to_seconds, format_time_length
from swiss_common_utils.utils.log.log_utils import get_logger, log_enter_and_exit

from django_model_builder_service.metrics.metrics import *

config_manager = None
builder_service = None
retention_service = None

logger = get_logger()


def generate_error_json_response(error):
    return JsonResponse({"error": error})


def generate_exception_error_message(e):
    return 'Exception caught. type: {}, message: {}'.format(type(e), str(e))


@log_enter_and_exit
def get_model(request):
    # metrics_dict[COUNTERS][GET_MODEL].inc()
    if request.method != 'GET':
        return generate_error_json_response('not a get request')

    try:
        global builder_service
        latest_model = builder_service.get_model_data()
        logger.info('Size of response: {} KB'.format(int(len(str(latest_model).encode('utf-8')) / 1024)))
        return JsonResponse(latest_model)
    except Exception as e:
        error_msg = generate_exception_error_message(e)
        logger.error(error_msg)
        return generate_error_json_response(error_msg)


@log_enter_and_exit
def build_model(params):
    try:
        global builder_service
        params['result'] = builder_service.build_model()

        global config_manager
        build_interval_seconds_str = config_manager.get_config_val_with_default('model_build_interval', '0.0s')
        build_interval_seconds = time_string_to_seconds(build_interval_seconds_str)
        logger.info('Model build interval: {}'.format(build_interval_seconds_str))
        if build_interval_seconds > 10.0:
            temp_params = {}
            t = threading.Timer(function=build_model, args=[temp_params], interval=build_interval_seconds)
            t.start()

    except Exception as e:
        msg = generate_exception_error_message(e)
        logger.error(msg)
        params['result'] = msg


@log_enter_and_exit
def do_retention():
    global retention_service
    retention_service.run()

    global config_manager
    retention_interval_str = config_manager.get_config_val_with_default('retention_interval',
                                                                        '1d')  # Default 1d
    retention_interval_seconds = time_string_to_seconds(retention_interval_str)
    logger.info('Model retention interval: {}'.format(retention_interval_str))
    if retention_interval_seconds > 10.0:
        t = threading.Timer(function=build_model, interval=retention_interval_seconds)
        t.start()


def show_model(request, identifier):
    # metrics_dict[COUNTERS][SHOW_MODEL].inc()

    from django_model_builder_service.models import PredictionModel
    model = get_object_or_404(PredictionModel, identifier=identifier)
    try:
        stats = json.loads(model.stats.replace("'", '"'))
        config = json.loads(model.config.replace("'", '"'))
    except Exception as e:
        logger.warning(generate_exception_error_message(e))
        stats = model.stats
        config = model.config

    my_tz = pytz.timezone('Israel')
    timezone.activate(my_tz)
    now = timezone.localtime()
    build_time = timezone.localtime(model.build_time)
    context = {
        'now': now.strftime('%d %B %Y, %H:%M:%S'),
        'identifier': identifier,
        'build_time': build_time.strftime('%d %B %Y, %H:%M:%S'),
        'stats': stats,
        'build_duration': format_time_length(seconds=model.build_duration),
        'config': config,
        'memory_usage': model.memory_usage
    }

    return render(request, 'service/model.html', context)
