import logging
import colorlog


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

    stream = logging.StreamHandler()
    stream.setLevel(_log_level)
    stream.setFormatter(formatter)

    log = logging.getLogger('pythonConfig')
    log.setLevel(_log_level)
    log.addHandler(stream)

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

