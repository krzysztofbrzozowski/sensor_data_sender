"""
@author:    Krzysztof Brzozowski
@file:      logger_sample_config
@time:      03/05/2022
@desc:      Logger configurator from YAML file
"""
import logging.config
import yaml
import os
import re
import colorlog

# Added path loader to load environment variable from in YAML file
path_matcher = re.compile(r'.*\$\{([^}^{]+)\}.*')


def path_constructor(loader, node):
    return os.path.expandvars(node.value)


class EnvVarLoader(yaml.SafeLoader):
    pass


EnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
EnvVarLoader.add_constructor('!path', path_constructor)


with open(os.path.join(
        os.getenv('SENSOR_DATA_SENDER_LOGGER_DIR', None), 'config_logger.yaml'), 'r') as f:
    config = yaml.load(f.read(), Loader=EnvVarLoader)
    logging.config.dictConfig(config)

logger = logging.getLogger('main_logger')

# TODO Remove Logger class, set up everything in yaml and remove all classmehotds from that -> log_error, log_warning etc.
class Logger:
    """
    Use:
    log.debug("A quirky message only developers care about")
    log.info("Curious users might want to know this")
    log.warn("Something is wrong and any user should be informed")
    log.error("Serious stuff, this is red for a reason")
    log.critical("OH NO everything is on fire")
    """
    _log_level = logging.DEBUG
    _log_format = '%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(asctime)s %(log_color)s| ' \
                  '%(log_color)s%(message)s%(reset)s'

    logging.root.setLevel(_log_level)
    formatter = colorlog.ColoredFormatter(_log_format)

    c_handler = logging.StreamHandler()
    c_handler.setLevel(_log_level)
    c_handler.setFormatter(formatter)

    log = logging.getLogger('pythonConfig')
    log.setLevel(_log_level)
    log.addHandler(c_handler)

    @classmethod
    def log_info(cls, msg: any) -> None:
        cls.log.info(msg)

    @classmethod
    def log_debug(cls, msg: any) -> None:
        cls.log.debug(msg)

    @classmethod
    def log_warning(cls, msg: any) -> None:
        cls.log.warning(msg)

    @classmethod
    def log_error(cls, msg: any) -> None:
        cls.log.error(msg)



def test_logs_backup_creation():
    import time
    for i in range(6):
        logger.debug("this is a debugging message")
        logger.info("this is an informational message")
        logger.warning("this is a warning message")
        logger.error("this is an error message")
        logger.critical("this is a critical message")
        try:
            c = 5 / 0
        except Exception as e:
            logger.exception('this is a exception message')

        time.sleep(1)


