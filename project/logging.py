
# from loguru import logger
# import sys

# def configure_logging():
#     logger.remove()
#     logger.add(sys.stderr, format="[ {time} : {level} ] [ {file}:{line} ] {message}", level="INFO")

# # Then, to log messages, you can use:
# # logger.info("This is an info message")
# # logger.error("This is an error message")




import logging
import logging.config


def configure_logging():
    logging_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[%(asctime)s: %(levelname)s] [%(pathname)s:%(lineno)d] %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "loggers": {
            "project": {
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.access": {
                "propagate": True,
            },
        },
    }

    logging.config.dictConfig(logging_dict)

