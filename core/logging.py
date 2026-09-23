CUSTOM_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"correlation_id": {"()": "core.logging_filters.CorrelationIdFilter"}},
    "formatters": {
        "simple": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(levelname)s %(message)s",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
        "verbose": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s [%(levelname)s] | [correlation_id=%(correlation_id)s] | %(asctime)s | %(name)s | %(message)s",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
        "json": {
            "format": '{"level": "%(levelname)s", "message": "%(message)s"}',
        },
    },
    "handlers": {
        # Best for cloud platforms (Docker, AWS ECS, Heroku, etc.)
        "console": {
            "level": "DEBUG",  # message level to be written to console
            # logging handler that outputs log messages to terminal
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["correlation_id"],
        },
        # Best for traditional server VPS deployments (DigitalOcean, EC2)
        # "file": {
        #     "level": "INFO",  # Keeps the production log file clean of verbose DB queries
        #     "class": "logging.handlers.RotatingFileHandler",
        #     "filename": os.path.join(PROJECT_PATH, "development.log"),
        #     "maxBytes": 1024 * 1024 * 10,  # 10 MB
        #     "backupCount": 5,
        #     "formatter": "verbose",
        # },
    },
    "loggers": {
        "": {
            # this sets root level logger to log info and higher level
            # logs to console. All other loggers inherit settings from
            # root level logger.
            "handlers": ["console"],
            "level": "INFO",
            # this tells logger to send logging message
            # to its parent (will send if set to True)
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        },
        "django.db": {
            # django also has database level logging
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "botocore": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "boto3": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "s3transfer": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "kombu": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "urllib3": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "httpx": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "httpcore": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "gtts": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
