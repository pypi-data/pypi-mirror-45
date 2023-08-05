#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Create by: @huongnhd
"""
import uuid
import os

import yaml
from comm.evar_logging import LogMsgERROR
from settings import GLOBAL_MAIN_TEMP_DIR


def prepare_tempdir_path():
    """
    prepare a tempdir for copy data
    assume that we have a preconfigured temp place
    assume that we use uuid to create a subtempdir

    :params
    :return
        - (string): path of temp dir just create
    """
    sub_temp_dir = str(uuid.uuid4())
    return os.path.join(GLOBAL_MAIN_TEMP_DIR, sub_temp_dir)


def load_file_yaml(file_path):
    """
    Load config from file yml to dict
    :params:
        - file_path(str):
    :returns:
        content(dict): content of file_path
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as yml_content:
            content = yaml.load(yml_content)
            return content
    else:
        # logger.error(LogMsgERROR.CAN_NOT_CONNECT % (file_path))
        raise ValueError(LogMsgERROR.CAN_NOT_CONNECT % file_path)

