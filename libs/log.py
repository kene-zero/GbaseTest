#!/bin/python3
# -*- coding:utf-8 -*-

import logging
import os.path

import colorlog

default_log_colors = {
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red'}


class Log:
    def __init__(self):
        """添加一个日志器"""

        self.file_f = colorlog.ColoredFormatter(
            fmt='%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]-%(levelname)s-[日志信息]: %(message)s',
            log_colors=default_log_colors)
        self.console_f = colorlog.ColoredFormatter(
            fmt='%(log_color)s%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]-%(levelname)s-[日志信息]: %(message)s',
            log_colors=default_log_colors)
        self.logger = logging.getLogger(__file__)
        self.logger.setLevel(logging.DEBUG)

        self.file_handler = self.get_file_handler("test.log")
        self.console_handler = self.get_console_handler()

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)

    def get_console_handler(self):
        """添加一个处理器"""
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(self.console_f)
        return handler

    def get_file_handler(self, file):
        """设置文件输出控制台"""
        import inspect
        case = inspect.stack()
        print(case)
        root_path = os.path.dirname(os.path.dirname(__file__))
        log_dir = os.path.join(root_path, "logs")
        log_file = os.path.join(log_dir, "test.log")
        file_handler = logging.FileHandler(filename=log_file, mode='a', encoding='UTF-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(self.file_f)
        return file_handler

    def get_logger(self):
        return self.logger


if __name__ == "__main__":
    log = Log().get_logger()
    log.info("hahaha")
    log.warning("hahaha")
    log.error("hahaha")
