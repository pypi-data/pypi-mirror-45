#!/usr/bin/env python3

"""Defines an easy function to set up a logger. """

import logging
import os

try:
    import colorlog
except ImportError:
    colorlog = None

clusterking_silence = "CLUSTERKING_SILENCE_ALL_LOGS"


def get_logger(name="Logger", level=logging.DEBUG, sh_level=logging.DEBUG):
    """Sets up a logging.Logger.

    If the colorlog module is available, the logger will use colors,
    otherwise it will be in b/w. The colorlog module is available at
    https://github.com/borntyping/python-colorlog but can also easily be
    installed with e.g. 'sudo pip3 colorlog' or similar commands.
    
    Args:
        name: name of the logger
        level: General logging level
        sh_level: Logging level of stream handler
    
    Returns:
        Logger
    """
    if colorlog:
        _logger = colorlog.getLogger(name)
    else:
        _logger = logging.getLogger(name)

    if _logger.handlers:
        # the logger already has handlers attached to it, even though
        # we didn't add it ==> logging.get_logger got us an existing
        # logger ==> we don't need to do anything
        return _logger

    _logger.setLevel(level)
    if os.environ.get("SILENCE_ALL_LOGS", False):
        _logger.setLevel(int(os.environ.get(clusterking_silence)))
    if colorlog is not None:
        sh = colorlog.StreamHandler()
        log_colors = {'DEBUG':    'cyan',
                      'INFO':     'green',
                      'WARNING':  'yellow',
                      'ERROR':    'red',
                      'CRITICAL': 'red'}
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(name)s:%(levelname)s:%(message)s',
            log_colors=log_colors)
    else:
        # no colorlog available:
        sh = logging.StreamHandler()
        formatter = logging.Formatter('%(name)s:%(levelname)s:%(message)s')
    sh.setFormatter(formatter)
    sh.setLevel(sh_level)
    _logger.addHandler(sh)

    if colorlog is None:
        _logger.debug("Module colorlog not available. Log will be b/w.")

    return _logger


def silence_all_logs(level=logging.WARNING):
    names = list(logging.root.manager.loggerDict.keys())
    names.append("DFMD")
    loggers = [
        logging.getLogger(name) for name in names
    ]
    for logger in loggers:
        logger.setLevel(level)
    os.environ[clusterking_silence] = str(logging.WARNING)


if __name__ == "__main__":
    # Test the color scheme for the logger.
    lg = get_logger("test")
    lg.debug("Test debug message")
    lg.info("Test info message")
    lg.warning("Test warning message")
    lg.error("Test error message")
    lg.critical("Test critical message")
