import atexit
import time
import scrapper.APIScrapper as api_scrapper
from apscheduler.schedulers.background import BackgroundScheduler

class APICronJob:

    def __init__(self):
        self._scheduler = BackgroundScheduler()
        self._api_scheduler = api_scrapper.APIScrapper()

    def start_api_job(self):
        # TODO: Refactor for better implementation
        api_scheduler = self._api_scheduler
        def api_call_job(sched):
            with sched as s:
                s.get_create_tickers_tables()
                print(s._tickers)

        self._scheduler.add_job(lambda: api_call_job(sched=api_scheduler), trigger='interval', seconds=3)
        self._scheduler.start()

