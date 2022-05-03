import logging
import colorlog


# class Logger:
#     """
#     Use:
#     log.debug("A quirky message only developers care about")
#     log.info("Curious users might want to know this")
#     log.warn("Something is wrong and any user should be informed")
#     log.error("Serious stuff, this is red for a reason")
#     log.critical("OH NO everything is on fire")
#     """
#     _log_level = logging.DEBUG
#     _log_format = '%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(asctime)s %(log_color)s| ' \
#                   '%(log_color)s%(message)s%(reset)s'
#
#     logging.root.setLevel(_log_level)
#     formatter = colorlog.ColoredFormatter(_log_format)
#
#     c_handler = logging.StreamHandler()
#     c_handler.setLevel(_log_level)
#     c_handler.setFormatter(formatter)
#
#     log = logging.getLogger('pythonConfig')
#     log.setLevel(_log_level)
#     log.addHandler(c_handler)
#
#     @classmethod
#     def log_info(cls, msg: any) -> None:
#         cls.log.info(msg)
#
#     @classmethod
#     def log_debug(cls, msg: any) -> None:
#         cls.log.debug(msg)
#
#     @classmethod
#     def log_warning(cls, msg: any) -> None:
#         cls.log.warning(msg)
#
#     @classmethod
#     def log_error(cls, msg: any) -> None:
#         cls.log.error(msg)
#

logging.root.setLevel(logging.DEBUG)

# Create a custom logger
logger = logging.getLogger('main_logger')

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.txt')

c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.DEBUG)

c_format = colorlog.ColoredFormatter(
    '%(log_color)s [%(levelname)-8s %(asctime)s.%(msecs)03d] %(message)s (%(filename)s:%(lineno)s)',
    datefmt='%Y-%m-%d %H:%M:%S')

f_format = logging.Formatter('[%(levelname)-8s %(asctime)s.%(msecs)03d] %(message)s (%(filename)s:%(lineno)s)',
                             datefmt='%Y-%m-%d %H:%M:%S')

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


logger.debug('Logger initialized')