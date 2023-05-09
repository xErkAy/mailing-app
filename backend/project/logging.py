import os
from project.settings import BASE_DIR

LOGS_DIR = os.path.join(BASE_DIR, 'logs')
if os.environ.get('LOGS_DIR', None):
    LOGS_DIR = os.environ.get('LOGS_DIR')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s %(process)d]: %(message)s',
        },
    },
    'handlers': {
        'mailing': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'mailing.log'),
            'formatter': 'standard',
        },
    },
    'loggers': {
        'mailing': {
            'handlers': ['mailing'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}