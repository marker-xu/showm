# -*- coding: utf-8 -*-
import time
import datetime
import os


def convert_encoding(data, from_encoding, to_encoding='UTF-8'):
    """
    字符串转码
    :param data: string
    :param from_encoding: string
    :param to_encoding: string
    :return: string
    """
    tmp = unicode(data, from_encoding, 'ignore').encode(to_encoding)
    return tmp


def file_put_contents(file_name, data):
    wh = open(file_name, "wb+")
    wh.write(data)
    wh.close()


def file_get_contents(file_name):
    wh = open(file_name, "rb+")
    result = wh.read()
    wh.close()
    return result


def str_to_time(date_string, date_format=None):
    if date_format is None:
        date_format = "%Y-%m-%d %H:%M:%S"
    time_list = time.strptime(date_string, date_format)
    time_stamp = int(time.mktime(time_list))
    return time_stamp


def time_to_string(time_stamp, date_format=None):
    """

    :param time_stamp: 
    :param date_format:
    :return:
    """
    date_list = datetime.datetime.utcfromtimestamp(time_stamp)
    if date_format is None:
        date_format = "%Y-%m-%d %H:%M:%S"
    date_string = date_list.strftime(date_format)
    return date_string


def mk_dir(path, ignore=True):
    """
    默认先检查目录是否存在
    :param path:
    :param ignore:
    :return:
    """
    if ignore is True and is_dir(path):
        return True
    os.makedirs(path)
    return True


def is_dir(path):
    """
    检查dir是否存在
    :param path: -> string
    :return: boolean
    """
    return os.path.exists(path=path)

