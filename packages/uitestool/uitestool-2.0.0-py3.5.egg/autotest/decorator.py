# code=utf-8

import os
import shutil
import logging
import time
from functools import wraps


def log(filename):
    def wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            logging.info("execution case in " + filename + "-->" + _wrapper.__name__)
            result = func(*args, **kwargs)
            # logging.info("execution case in " + filename +"-->" +_wrapper.__name__)
            return result
        return _wrapper
    return wrapper


def clear_dir(dir):
    def wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            for entry in os.scandir(dir):
                if entry.name.startswith('.'):
                    continue
                if entry.is_file():
                    os.remove(entry.path)  # 删除文件
                else:
                    shutil.rmtree(entry.path)  # 删除目录
            result = func(*args, **kwargs)
            return result
        return _wrapper
    return wrapper


