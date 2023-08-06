from apscheduler.schedulers.background import BackgroundScheduler
from swiss_common_utils.log.log_utils import get_logger


class ScheduleTaskManager:
    logger = get_logger()

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        self.tasks = {}

    def __del__(self):
        self.scheduler.shutdown(wait=False)

    def add_task(self, name, interval, func, next_run_time=None):
        if name in self.tasks:
            self.logger.error('task <{}> already exist'.format(name))
            return

        if next_run_time:
            self.tasks[name] = self.scheduler.add_job(func, 'interval', seconds=interval, next_run_time=next_run_time)
        else:
            self.tasks[name] = self.scheduler.add_job(func, 'interval', seconds=interval)

    def remove_task(self, name):
        if name not in self.tasks:
            self.logger.warning('Trying to remove non-existing task <{}>'.format(name))
            return

        self.tasks[name].remove()
        del self.tasks[name]

    def pause_task(self, name):
        job = self.__get_job(name)
        if not job:
            self.logger.error('Failed pausing task <{}>'.format(name))
            return

        job.pause()

    def resume_job(self, name):
        job = self.__get_job(name)
        if not job:
            self.logger.error('Failed resuming task <{}>'.format(name))
            return

        job.resume()

    def __get_job(self, name):
        if name not in self.tasks:
            self.logger.error('No such task <{}>'.format(name))
            return None

        return self.tasks[name]

    def get_task_next_run_time(self, name):
        job = self.__get_job(name)
        if not job:
            return

        return job.next_run_time

    def get_tasks_names(self):
        return self.tasks.keys()
