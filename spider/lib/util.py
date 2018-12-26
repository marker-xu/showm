# -*- coding: utf-8 -*-
import time, datetime
import requests
import re
import logging

REQUEST_TYPE_GET = 'get'
REQUEST_TYPE_POST = 'post'
REQUEST_TYPE_PUT = 'put'
REQUEST_TYPE_DELETE = 'delete'


def run_time(func):
    def wrapper(*args, **kw):
        start = time.time()
        result = func(*args, **kw)
        end = time.time()
        print('running', end-start, 's')
        logging.info('running: %ds' % (end-start))
        return result
    return wrapper


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
    date_list = datetime.datetime.utcfromtimestamp(time_stamp)
    if date_format is None:
        date_format = "%Y-%m-%d %H:%M:%S"
    date_string = date_list.strftime(date_format)
    return date_string


@run_time
def curl(url, params=None, headers=None, encoding="gb2312"):
    if params is None:
        params = {}

    if headers is None:
        headers = {}
    r = requests.get(url, params=params, headers=headers)
    encoding = encoding.lower()
    if encoding != "utf8" and encoding != "utf-8":
        s = convert_encoding(r.content, encoding, "utf8")
    else:
        s = r.content

    return s


def curl_common(url, params=None, headers=None, request_type=REQUEST_TYPE_GET, body=None):
    if params is None:
        params = {}

    if headers is None:
        headers = {}
    if request_type == REQUEST_TYPE_GET:
        r = requests.get(url, params=params, headers=headers)
    elif request_type == REQUEST_TYPE_POST:
        r = requests.post(url=url, params=params, headers=headers, data=body)

    if r.status_code == 200:
        return r.content
    else:
        r.raise_for_status()
