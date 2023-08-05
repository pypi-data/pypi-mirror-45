#!/usr/bin/env python3
# coding=utf-8

"""
@author: guoyanfeng
@software: PyCharm
@time: 18-12-26 下午3:32
"""
import asyncio
import multiprocessing
import sys
from collections import MutableMapping, MutableSequence
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

import aelog
import yaml
from bson import ObjectId

from aclients.exceptions import Error, FuncArgsError

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

__all__ = ("ignore_error", "verify_message", "wrap_async_func", "analysis_yaml", "gen_class_name", "objectid")

# 执行任务的线程池
pool = ThreadPoolExecutor(multiprocessing.cpu_count() * 10 + multiprocessing.cpu_count())


@contextmanager
def ignore_error(error=Exception):
    """
    个别情况下会忽略遇到的错误
    Args:

    Returns:

    """
    try:
        yield
    except error as e:
        aelog.warning(e)


def verify_message(src_message: dict, message: list or dict):
    """
    对用户提供的message进行校验
    Args:
        src_message: 默认提供的消息内容
        message: 指定的消息内容
    Returns:

    """
    src_message = dict(src_message)
    message = message if isinstance(message, MutableSequence) else [message]
    required_field = {"msg_code", "msg_zh", "msg_en"}

    for msg in message:
        if isinstance(msg, MutableMapping):
            if set(msg.keys()).intersection(required_field) == required_field and msg["msg_code"] in src_message:
                src_message[msg["msg_code"]].update(msg)
    return src_message


async def wrap_async_func(func, *args, **kwargs):
    """
    包装同步阻塞请求为异步非阻塞
    Args:
        func: 实际请求的函数名或者方法名
        args: 函数参数
        kwargs: 函数参数
    Returns:
        返回执行后的结果
    """
    try:
        result = await asyncio.wrap_future(pool.submit(func, *args, **kwargs))
    except TypeError as e:
        raise FuncArgsError("Args error: {}".format(e))
    except Exception as e:
        raise Error("Error: {}".format(e))
    else:
        return result


def gen_class_name(underline_name):
    """
    由下划线的名称变为驼峰的名称
    Args:
        underline_name
    Returns:

    """
    return "".join([name.capitalize() for name in underline_name.split("_")])


def analysis_yaml(full_conf_path):
    """
    解析yaml文件
    Args:
        full_conf_path: yaml配置文件路径
    Returns:

    """
    with open(full_conf_path, 'rt', encoding="utf8") as f:
        try:
            conf = yaml.load(f, Loader=Loader)
        except yaml.YAMLError as e:
            print("Yaml配置文件出错, {}".format(e))
            sys.exit()
    return conf


def objectid():
    """

    Args:

    Returns:

    """
    return str(ObjectId())
