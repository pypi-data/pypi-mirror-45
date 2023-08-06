import base64
import io
import pickle

from memory_profiler import profile
from swiss_common_utils.datetime.datetime_utils import format_time_length
from swiss_common_utils.log.log_utils import get_logger, log_enter_and_exit, print_ascii_art
from swiss_common_utils.sync.mrow_lock.mrow import RWLock

from django_model_builder_service import app_globals
from django_model_builder_service.exceptions.ModelNotBuildError import ModelNotBuildError

memory_usage_stream_build_model = io.StringIO('')


class BuilderService:
    logger = get_logger()
    mrow_lock = RWLock()

    def lock(type):
        def wrap(org_func):
            def wrapped_func(self, *args, **kwargs):
                self.logger.debug('acquiring {} lock'.format(type))

                lock = self.mrow_lock.get_lock(type)

                try:
                    result = org_func(self, *args, **kwargs)
                finally:
                    lock.release()
                    self.logger.debug('releasing {} lock'.format(type))

                return result

            return wrapped_func

        return wrap

    def __init__(self, prediction_model_wrapper, config_manager):
        self.model_data = None

        self.config_manager = config_manager

        self.wrapper = prediction_model_wrapper

    @lock(type='reader')
    def __get_model_data(self):
        return self.model_data

    @lock(type='writer')
    def __set_model_data(self, model_data):
        self.model_data = model_data

    @log_enter_and_exit
    def _save_model_to_db(self):
        try:
            model_data = self.__get_model_data()

            if model_data:
                identifier = model_data.identifier
                self.logger.info('saving model {} to db'.format(identifier))
                self.logger.info('DB engine: {}'.format(
                    self.config_manager.get_config_val_with_default('settings_db_engine',
                                                                    'Not configured!!!')))
                from django_model_builder_service.models import PredictionModel
                pickled_model = pickle.dumps(model_data.model)
                global memory_usage_stream_build_model
                PredictionModel.objects.create(model=pickled_model,
                                               identifier=identifier,
                                               build_time=model_data.build_time,
                                               stats=model_data.stats,
                                               build_duration=model_data.build_duration,
                                               config=self.config_manager.get_config_val_with_default('model', '{}'),
                                               memory_usage=memory_usage_stream_build_model.getvalue())
                self.logger.info('saving model {} to db - DONE'.format(identifier))

        except Exception as e:
            self.logger.exception(msg='Exception caught. type: {}, message: {}'.format(type(e), str(e)))

    def __encode_model(self, trained_model_data):
        model = trained_model_data.model
        model = pickle.dumps(model)
        model_enc = base64.b64encode(model)
        trained_model_data.model = model_enc.decode(
            'utf-8')  # Convert byte string to string (for json serialization to send over the network)
        return trained_model_data

    @profile(stream=memory_usage_stream_build_model)
    def __build_model_with_memory_profiling(self):
        return self.wrapper.build()

    def __collect_trained_model_metrics(self, trained_model_data):
        GENERAL = 'general'
        ACCURACY = 'accuracy'
        ERROR_RATE = 'error_rate'
        TRAIN_SET_SIZE = 'train_set_size'
        TEST_SET_SIZE = 'test_set_size'
        DATASET_SIZE = 'dataset_size'

        app_globals.metrics_registrar.gauge(name='build_duration', documentation='model duration time metric').set(
            trained_model_data.build_duration)

        if GENERAL in trained_model_data.stats:
            general_model_stats = trained_model_data.stats[GENERAL]
            if ACCURACY in general_model_stats:
                app_globals.metrics_registrar.gauge(name=ACCURACY, documentation='model accuracy metric').set(
                    general_model_stats[ACCURACY])
            if ERROR_RATE in general_model_stats:
                app_globals.metrics_registrar.gauge(name=ERROR_RATE, documentation='model error rate metric').set(
                    general_model_stats[ERROR_RATE])
            if TRAIN_SET_SIZE in general_model_stats:
                app_globals.metrics_registrar.gauge(name=TRAIN_SET_SIZE,
                                                    documentation='model train set size metric').set(
                    general_model_stats[TRAIN_SET_SIZE])
            if TEST_SET_SIZE in general_model_stats:
                app_globals.metrics_registrar.gauge(name=TEST_SET_SIZE, documentation='model test set size metric').set(
                    general_model_stats[TEST_SET_SIZE])
            if DATASET_SIZE in general_model_stats:
                app_globals.metrics_registrar.gauge(name=DATASET_SIZE, documentation='model dataset size metric').set(
                    general_model_stats[DATASET_SIZE])

    @log_enter_and_exit
    def build_model(self):
        print_ascii_art('BUILD MODEL')
        trained_model_data = self.__build_model_with_memory_profiling()
        trained_model_data = self.__encode_model(trained_model_data)
        self.__set_model_data(trained_model_data)
        self._save_model_to_db()
        self.logger.info('new model identifier: {}'.format(trained_model_data.identifier))
        self.logger.info('new model build time: {}'.format(trained_model_data.build_time))
        self.logger.info(
            'new model build duration: {}'.format(format_time_length(seconds=trained_model_data.build_duration)))
        global memory_usage_stream_build_model
        memory_usage_stream_build_model.seek(0)  # Set the file pointer back to 0 so old report is overwritten
        memory_usage_str = memory_usage_stream_build_model.getvalue()
        self.logger.info('Memory usage summary: {}'.format(memory_usage_str))

        self.__collect_trained_model_metrics(trained_model_data=trained_model_data)

        return True

    @log_enter_and_exit
    def get_model_data(self):
        self.logger.info('Getting model...')
        model_data = self.__get_model_data()

        if model_data:
            self.logger.info('model identifier: {}'.format(model_data.identifier))
            self.logger.info('model build time: {}'.format(model_data.build_time))
            return model_data

        raise ModelNotBuildError('no model was build yet')
