#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import json
import logging
import os
from model.dao.topic import *
from model.data.topic import *
from model.request.data import *
from model.response.data import *
from lib.util import *
from lib.exception import BizException

from tornado.options import define, options

define("port", default=8494, help="run on the given port", type=int)
define("base_path", default=os.path.dirname(__file__),
       help="run on the given path",
       type=basestring)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class ApiHandler(tornado.web.RequestHandler):

    _response = {}
    _model_topic = None

    def initialize(self):
        self._model_topic = ModelDataTopic()

        self._response = {
            'code': 0,
            'result': None,
            'message': '',
        }

    def get(self):
        self.process_request()

    def post(self):
        self.process_request()

    def _make_response(self, code=0, message='', result=None):
        """

        :param code: -> int
        :param message: -> string
        :param result: -> mixed
        :return: -> None
        """
        self._response['code'] = code
        self._response['message'] = message
        self._response['result'] = result
        logging.info('response, %s' % json.dumps(self._response))
        self.write(json.dumps(self._response))

    def process_request(self):
        method = self.get_argument('method', None)
        params = self.get_argument('params', None)
        version = self.get_argument('version', default=1.0)
        logging.info('request start, method-%s, version-%s, params-%s'
                     % (method, version, params))
        allow_method_list = ['add_topic', 'add_pictures', 'add_picture_content',
                             'get_picture_list', 'check_topic_exists',
                             'update_stat', 'add_picture_detect']
        if method is None:
            self._make_response(code=1, message='method is empty')
        elif method in allow_method_list:
            func = getattr(self, method)
            func(params)
        else:
            self._make_response(code=1, message='method not exists')

    def add_topic(self, params):
        """

        :param params: dict
        :return: void
        """
        json_params = json.loads(params)
        request = RequestAddTopic()
        request.make_request(json_params)
        request.org_topic_id = json_params['topic_id'].strip()
        qq = 0
        weixin = email = ""
        if json_params["contact"]["qq"] is not None:
            qq = json_params["contact"]["qq"]
        if json_params["contact"]["weixin"] is not None:
            weixin = json_params["contact"]["weixin"]
        if json_params["contact"]["email"] is not None:
            email = json_params["contact"]["email"]
        request.qq = qq
        request.weixin = weixin
        request.email = email
        request.post_time = json_params['create_time']
        try:
            response = self._model_topic.add_topic(request)
        except BizException, e:
            logging.info('error: %s' % (e.message, ))
            self._make_response(code=1, message='topic has exists')
            return False

        self._make_response(result=response.result)

    def check_topic_exists(self, params):
        """

        :param params: -> dict
        :return:
        """
        json_params = json.loads(params)
        request = RequestGetTopic()
        request.org_topic_id = json_params['topic_id'].strip()
        request.topic_from = json_params['topic_from']
        response = self._model_topic.get_topic(request)
        tmp_result = False
        if response.result is not None:
            tmp_result = True
        self._make_response(result=tmp_result)

    def add_pictures(self, params):
        json_params = json.loads(params)
        request = RequestAddPictures()
        request.topic_id = json_params['id']
        request.org_topic_id = json_params['topic_id'].strip()
        request.topic_from = json_params['topic_from']
        request.pic_list = json_params['pic_list']
        response = self._model_topic.add_pictures(request=request)
        self._make_response(result=response.result)

    def add_picture_content(self, params):
        json_params = json.loads(params)
        request = RequestAddPictureContent()

        request.id = int(json_params['id'])
        request.content = self.request.body
        try:
            response = self._model_topic.add_picture_content(request=request)
        except BizException, e:
            logging.info('error: %s' % (e.message, ))
            self._make_response(code=1, message='picture id not exists')
            return False
        self._make_response(result=response.result)

    def get_picture_list(self, params):
        json_params = json.loads(params)
        request = RequestGetPictureList()
        request.make_request(json_params)
        response = self._model_topic.get_picture_list(request)
        self._make_response(result=response.result)

    def get_picture_total(self, params):
        json_params = json.loads(params)
        request = RequestGetPictureTotal()
        request.make_request(json_params)
        response = self._model_topic.get_picture_total(request=request)
        self._make_response(result=response.result)

    def update_stat(self, params):
        json_params = json.loads(params)
        request = RequestUpdateStat()
        request.make_request(json_params)
        request.org_topic_id = json_params['topic_id'].strip()
        response = self._model_topic.update_stat(request)
        self._make_response(result=response.result)

    def add_picture_detect(self, params):
        json_params = json.loads(params)
        request = RequestAddPictureDetect()
        request.make_request(json_params)
        response = self._model_topic.add_picture_detect(request=request)
        self._make_response(result=response.result)


def main():
    logging.basicConfig(filename=os.path.join(options.base_path, "log", "info.log"),
                        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s:"
                               "%(pathname)s:%(lineno)d")
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/api", ApiHandler),
    ], static_path=os.path.join(options.base_path, "static"))
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
