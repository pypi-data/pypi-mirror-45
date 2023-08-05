#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Create by: @huongnhd
"""
import os
import logging

import yaml
from logging import config
from settings import RUN_MODE, BASE_DIR


def setup_logging(
        default_path= os.path.join(BASE_DIR,'conf/logging.yml'),
        default_level=logging.INFO,
        env_key='LOG_CFG'):
    """Setup logging configuration
       IF using LOG_CFG is env variable
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as file_config:
            config_logging = yaml.safe_load(file_config.read())
        logging.config.dictConfig(config_logging)
    else:
        logging.basicConfig(level=default_level)




class LogMsgHistory:
    """Define name message for log history"""

    APP_START_MSG = u'[001] start [%s]'
    APP_END_MSG = u'[002] end [%s]'
    ENCRICHMENT_START_MSG = u'[003] start encrichment [%s]'
    ENCRICHMENT_END_MSG = u'[004] end encrichment [%s]'


class LogMsgERROR:
    """Define name message for log error"""

    CAN_NOT_CONNECT = u'[005] can not connect to [%s]'
    FILE_NOT_FOUND = u'[008] file [%s] not found'

# load the logging configuration
setup_logging()

if RUN_MODE == 'PRODUCTION':
    LOGGER = logging.getLogger('application')
    LOGGER_HISTORY = logging.getLogger('history')
else:
    # RUN_MODE = 'DEV'
    LOGGER = LOGGER_HISTORY = logging.getLogger('screen')
