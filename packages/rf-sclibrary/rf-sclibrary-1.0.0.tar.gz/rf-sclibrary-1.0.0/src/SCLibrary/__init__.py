# -*- coding:utf-8 -*-
from gevent import monkey
monkey.patch_all()

from SCLibrary.base import DynamicCore, hook_zh
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from SCLibrary.builtin import SelectKeywords
from SCLibrary.builtin import RandomKeywords
from SCLibrary.builtin import LogListener
from SCLibrary.builtin import DBKeywords
from SCLibrary.builtin import LocustKeyword
from SCLibrary.builtin import RequesterKeywords
from SCLibrary.builtin import ValidatorKeywords
import os

__version__ = '1.0.0'

class SCLibrary(DynamicCore):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        libraries = [ValidatorKeywords(), RequesterKeywords(),
                     DBKeywords(), RandomKeywords(), SelectKeywords(), LocustKeyword()]
        DynamicCore.__init__(self, libraries)
        built_in = BuiltIn()
        if built_in.get_variable_value("${RF_DEBUG}") == True:
            self.ROBOT_LIBRARY_LISTENER = LogListener()
        # 复写robot的unic.py，支持Log打印中文
        # hook_zh()
