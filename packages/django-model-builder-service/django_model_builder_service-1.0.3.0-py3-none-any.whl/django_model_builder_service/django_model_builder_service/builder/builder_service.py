import base64
import io
import pickle

from memory_profiler import profile
from swiss_common_utils.utils.datetime.datetime_utils import format_time_length
from swiss_common_utils.utils.log.log_utils import log_enter_and_exit, get_logger, print_ascii_art

from django_model_builder_service.django_model_builder_service.builder.mrow_lock.mrow import RWLock

memory_usage_stream_build_model = io.StringIO('')


class BuilderService:
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

    def __init__(self, config_manager):
        self.model_data = None

        self.config_manager = config_manager

        config_dict = self.config_manager.get_config_dict()

        # TODO: expose func to register the wrapper
        self.wrapper = PredictionModelWrapper(config_dict)

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
                identifier = model_data['identifier']
                self.logger.info('saving model {} to db'.format(identifier))
                from django_model_builder_service.models import PredictionModel
                pickled_model = pickle.dumps(model_data['model'])
                global memory_usage_stream_build_model
                PredictionModel.objects.create(model=pickled_model,
                                               identifier=identifier,
                                               build_time=model_data['build_time'],
                                               stats=model_data['stats'],
                                               build_duration=model_data['build_duration'],
                                               config=self.config_manager.get_config_val_with_default('model', '{}'),
                                               memory_usage=memory_usage_stream_build_model.getvalue())
                self.logger.info('saving model {} to db - DONE'.format(identifier))

        except Exception as e:
            self.logger.error('Exception caught. type: {}, message: {}'.format(type(e), str(e)))

    def __encode_model(self, model_data):
        model = model_data['model']
        model_enc = base64.b64encode(model)
        model_data['model'] = model_enc.decode(
            'utf-8')  # Convert byte string to string (for json serialization to send over the network)
        return model_data

    @profile(stream=memory_usage_stream_build_model)
    def __build_model_with_memory_profiling(self):
        return self.wrapper.build()

    @log_enter_and_exit
    def build_model(self):
        print_ascii_art('BUILD MODEL')
        model_data = self.__build_model_with_memory_profiling()
        model_data = self.__encode_model(model_data)
        self.__set_model_data(model_data)
        self._save_model_to_db()
        self.logger.info('new model identifier: {}'.format(model_data['identifier']))
        self.logger.info('new model build time: {}'.format(model_data['build_time']))
        self.logger.info(
            'new model build duration: {}'.format(format_time_length(seconds=model_data['build_duration'])))
        global memory_usage_stream_build_model
        memory_usage_stream_build_model.seek(0)  # Set the file pointer back to 0 so old report is overwritten
        memory_usage_str = memory_usage_stream_build_model.getvalue()
        self.logger.info('Memory usage summary: {}'.format(memory_usage_str))

        return True

    @log_enter_and_exit
    def get_model_data(self):
        self.logger.info('Getting model...')
        model_data = self.__get_model_data()

        if model_data:
            self.logger.info('model identifier: {}'.format(model_data['identifier']))
            self.logger.info('model build time: {}'.format(model_data['build_time']))
            return model_data

        raise ModelNotBuildError('no model was build yet')
