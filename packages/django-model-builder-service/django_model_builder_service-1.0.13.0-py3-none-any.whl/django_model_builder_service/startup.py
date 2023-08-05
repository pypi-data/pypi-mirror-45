import os
import sys
import threading

from prometheus_client import Counter
from swiss_common_utils.utils.datetime.datetime_utils import time_string_to_seconds
from swiss_common_utils.utils.log.log_utils import get_logger, log_enter_and_exit
from swiss_common_utils.utils.yml.yaml_utils import yaml_to_flat_dict

from django_model_builder_service.django_model_builder_service import views
from django_model_builder_service.django_model_builder_service.builder.builder_service import BuilderService
from django_model_builder_service.django_model_builder_service.config.config_manager import ConfigManager
from django_model_builder_service.django_model_builder_service.metrics.metrics import *
from django_model_builder_service.django_model_builder_service.views import build_model, do_retention

logger = get_logger()


def initialize_retention_service():
    retention_interval_str = views.config_manager.get_config_val_with_default('retention_interval',
                                                                              '1d')  # Default is 1d
    retention_interval_seconds = time_string_to_seconds(retention_interval_str)

    retention_shelf_life_str = views.config_manager.get_config_val_with_default('retention_shelf_life',
                                                                                '3d')  # Default is 3d
    retention_shelf_life_seconds = time_string_to_seconds(retention_shelf_life_str)
    retention_shelf_life_minutes = retention_shelf_life_seconds / 60

    logger.info(
        'Initializing retention. Interval: {}, Shelf life: {}'.format(retention_interval_str,
                                                                      retention_shelf_life_str))

    from django_model_builder_service.django_model_builder_service.retention.retention import RetentionService
    views.retention_service = RetentionService(shelf_life_minutes=retention_shelf_life_minutes)

    t = threading.Timer(retention_interval_seconds, do_retention)
    t.start()


def initialize_config_manager():
    views.config_manager = ConfigManager()


def initialize_builder_service(prediction_model_wrapper):
    views.builder_service = BuilderService(prediction_model_wrapper=prediction_model_wrapper,
                                           config_manager=views.config_manager)


def is_debug():
    try:
        return os.environ['CONFIG_SERVICE_SETTINGS_DEBUG'].lower() == 'true'
    except KeyError as e:
        logger.warning('No environment variable: CONFIG_SERVICE_SETTINGS_DEBUG. setting default value: True'.format())
        return True


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


def initialize_build_model_task():
    # Build first model (blocking)
    params = {}
    t = threading.Timer(0.0, build_model, args=[params])
    t.start()


def initialize_metrics_counters():
    metrics_dict[COUNTERS][SHOW_MODEL] = Counter(name='show_model', documentation='count calls for model show')
    metrics_dict[COUNTERS][GET_MODEL] = Counter(name='get_model', documentation='count calls for get model')


# Initialize all tasks here
@log_enter_and_exit
def initializae_background_tasks(prediction_model_wrapper):
    # migrate & test command may not finish due to the recurring task initialized next.
    # Initialize the recurring task only on runserver command
    if not should_start_initialize_sequence():
        return

    logger.info('Running initializing sequence for service app')

    # Initialization order matters - do not change!
    initialize_config_manager()
    prediction_model_wrapper.config = views.config_manager.get_config_dict()
    initialize_builder_service(prediction_model_wrapper=prediction_model_wrapper)
    initialize_metrics_counters()
    initialize_retention_service()
    initialize_build_model_task()
