from unittest import TestCase, mock

from django_model_builder_service.services.builder.builder import BuilderService
from django_model_builder_service.config.config_manager import ConfigManager


class TestBuilderService(TestCase):

    def test_model_data_verify_saving_old_model_verify_wrapper_build(self):
        class MockWrapper:
            def build(self):
                pass

        wrapper = MockWrapper()

        builder_service = BuilderService(prediction_model_wrapper=wrapper, config_manager=ConfigManager())
        with mock.patch.object(builder_service, '_save_model_to_db') as mock_save_old_model:
            with mock.patch.object(builder_service.wrapper, 'build') as mock_wrapper_build:
                mock_wrapper_build.return_value = {
                    'model': b'test_model',
                    'identifier': 'test_identifier',
                    'build_time': 'test_build_time',
                    'build_duration': 777
                }
                builder_service.build_model()
                self.assertEquals(mock_save_old_model.call_count, 1)
                self.assertEqual(mock_wrapper_build.call_count, 1)
