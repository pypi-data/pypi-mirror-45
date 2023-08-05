from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.management import call_command

import sys
import time
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from logutils.colorize import ColorizingStreamHandler


class ColorHandler(ColorizingStreamHandler):
    def __init__(self, *args, **kwargs):
        super(ColorHandler, self).__init__(*args, **kwargs)
        self.level_map = {
            logging.DEBUG: (None, 'blue', False),
            logging.INFO: (None, 'green', False),
            logging.WARNING: (None, 'yellow', False),
            logging.ERROR: (None, 'red', False),
            logging.CRITICAL: ('red', 'white', True),
        }

CONFIG = {
    'version':1,
    'disable_existing_loggers': True,
    'handlers':{
        'console': {
            '()':ColorHandler,
            # 'info':'white',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout',
        },
    },
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(module)s line:%(lineno)-4d %(levelname)-8s %(message)s',
        },
    },
    'loggers': {
        '': {
            'level':'DEBUG',
            'handlers':['console'],
        },
    },
}

logging.config.dictConfig(CONFIG)
logger = logging.getLogger('')


class EventHandler(LoggingEventHandler):
    wait = False

    def dispatch(self, event):
        super(EventHandler, self).dispatch(event)
        if self.wait:
            return

        self.wait = True
        self.setTimeout(self.run_collectstatic, 0.5)

    def run_collectstatic(self):
        call_command('collectstatic', interactive=False)
        self.wait = False

    def setTimeout(self, func, seconds):
        timer = threading.Timer(seconds, func)
        timer.start()

    # def on_moved(self, event):
    #     what = 'directory' if event.is_directory else 'file'
    #     logger.warn("Moved %s: from %s to %s", what, event.src_path, event.dest_path)

    # def on_created(self, event):
    #     what = 'directory' if event.is_directory else 'file'
    #     logger.info("Created %s: %s", what, event.src_path)

    # def on_delete(self, event):
    #     print("on_delete")
    #     what = 'directory' if event.is_directory else 'file'
    #     logger.error("Deleted %s: %s", what, event.src_path)

    # def on_modified(self, event):
    #     what = 'directory' if event.is_directory else 'file'
    #     logger.warn("Modified %s: %s", what, event.src_path)


class Command(BaseCommand):
    help = 'Daemon to watch static files and collect them automatically'

    def handle(self, *args, **options):
        try:
            path = settings.BASE_DIR
        except AttributeError:
            path = '.'

        logger.info("Watching: %s", path)
        event_handler = EventHandler()
        observer = Observer()
#)
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
