import atexit
import time
import scrapper.APIScrapper as api_scrapper
from apscheduler.schedulers.background import BackgroundScheduler
import sp500.list_scrapper as sp500

class APICronJob:

    def __init__(self):
        self._scheduler = BackgroundScheduler()
        self._api_scheduler = api_scrapper.APIScrapper()
        # Init SP500 db and its ticker tables
        sp500.store_to_db(sp500.pull_sp500_stocks())
        # Init _api_scheduler with tickers from db at cron job creation and data from 2000-01-01
        with self._api_scheduler as s:
            s.get_create_tickers_tables()
            s.drop_refill_database()

    def start_api_job(self):
        api_scheduler = self._api_scheduler
        def api_call_job(sched):
            with sched as s:
                s.fill_database_from_last()

        self._scheduler.add_job(lambda: api_call_job(sched=api_scheduler), trigger='cron', day_of_week='mon-fri', hour=23, minute=59)
        self._scheduler.start()

