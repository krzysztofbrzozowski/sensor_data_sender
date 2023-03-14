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

# Added path loader to load environment variable from in YAML file
path_matcher = re.compile(r'.*\$\{([^}^{]+)\}.*')


def path_constructor(loader, node):
    return os.path.expandvars(node.value)


class EnvVarLoader(yaml.SafeLoader):
    pass


EnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
EnvVarLoader.add_constructor('!path', path_constructor)


with open(os.path.join(
        os.getenv('SENSOR_DATA_SENDER_LOGGER_DIR', None), '../config/config_logger.yaml'), 'r') as f:
    config = yaml.load(f.read(), Loader=EnvVarLoader)
    logging.config.dictConfig(config)

logger = logging.getLogger('main_logger')


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


