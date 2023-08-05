import datetime
from swiss_common_utils.utils.log.log_utils import get_logger, log_enter_and_exit, print_ascii_art


class RetentionService:
    logger = get_logger()

    def __init__(self, shelf_life_minutes=4320):
        self.shelf_life_minutes = shelf_life_minutes

    @log_enter_and_exit
    def run(self):
        print_ascii_art('RETENTION')
        deletion_time = datetime.datetime.now() - datetime.timedelta(minutes=self.shelf_life_minutes)

        self.logger.info('Deleting models built before: {}'.format(deletion_time.strftime('%Y-%m-%d %H:%M')))

        from django_model_builder_service.models import PredictionModel
        records_deleted, queryset = PredictionModel.objects.filter(build_time__lt=deletion_time).delete()
        self.logger.info('Deleted {} models from db'.format(records_deleted))
