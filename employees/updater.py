from apscheduler.schedulers.background import BackgroundScheduler
from .task import update_something
import os

def start():
    if os.environ.get('RUN_MAIN'):
        scheduler = BackgroundScheduler()
        scheduler.add_job(update_something, 'interval', seconds=10)
        scheduler.start()