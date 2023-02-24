# Dictionary is use for generate all logs according to syetem generating
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # Format of log
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(filename)s %(funcName)s  %(message)s'
        },
    },
    # handle specific logs according to level
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/Info.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        }
    },
    # for control all handler, level, logs etc
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level':"INFO",
            'propagate': True
        },
    },
}