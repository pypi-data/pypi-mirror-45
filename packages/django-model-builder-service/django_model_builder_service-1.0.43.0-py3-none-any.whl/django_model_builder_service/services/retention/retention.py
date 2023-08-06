import datetime

from swiss_common_utils.datetime.datetime_utils import time_string_to_seconds
from swiss_logger.log_utils import log_enter_and_exit, print_ascii_art

from django_model_builder_service.common.logger import get_logger


class RetentionService:
    logger = get_logger()

    def __init__(self, config_manager):
        self.config_manager = config_manager

        retention_shelf_life_str = self.config_manager.get_config_val_with_default(
            'retention_shelf_life', '3d')  # Default is 3d
        retention_shelf_life_seconds = time_string_to_seconds(retention_shelf_life_str)
        retention_shelf_life_minutes = retention_shelf_life_seconds / 60

        self.logger.info(
            'Initializing retention service. Shelf life: {}'.format(retention_shelf_life_str))

        self.shelf_life_minutes = retention_shelf_life_minutes

    @log_enter_and_exit
    def run(self):
        print_ascii_art('RETENTION')
        deletion_time = datetime.datetime.now() - datetime.timedelta(minutes=self.shelf_life_minutes)

        self.logger.info('Deleting models built before: {}'.format(deletion_time.strftime('%Y-%m-%d %H:%M')))

        from django_model_builder_service.models import PredictionModel
        records_deleted, queryset = PredictionModel.objects.filter(build_time__lt=deletion_time).delete()
        self.logger.info('Deleted {} models from db'.format(records_deleted))
