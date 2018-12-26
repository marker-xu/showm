# -*- coding: utf-8 -*-
import logging
import time
import base64
from lib.util import *
from model.topic import *
from sdk.aip import AipFace


class Picture(object):

    _call_api_path = ''

    _host_map = {}

    _aip_conf = {}

    _aip_client = None

    def __init__(self):
        self._call_api_path = 'http://cp01-rdqa-dev005-xucongbin.epc.baidu.com:8494/api'
        self._host_map = {
            SOURCE_FUDAN: 'https://bbs.fudan.sh.cn',
            SOURCE_NJU: 'http://bbs.nju.edu.cn',
            SOURCE_SJTU: 'https://bbs.sjtu.edu.cn',
            SOURCE_QINGHUA: 'http://att.newsmth.net',
        }
        self._aip_conf = {
            'app_id': '10121651',
            'api_key': 'pWF9SzypaaqEiAGNCu9FFkfL',
            'secret_key': 'OIOvTm1KS0GZKWOE5VWdGiAnzElrB6Zh',
        }
        self._init_aip_client()

    def get_list(self, topic_from=None):
        """

        :return: list
        """
        url = self._call_api_path
        method = 'get_picture_list'
        params = {
            'status': 1,
        }
        if topic_from is not None:
            params['topic_from'] = topic_from
        params_struct = {
            'method': method,
            'params': json.dumps(params),
        }
        response = curl_common(url, params=params_struct)
        ret = json.loads(response)
        if 'code' in ret and ret['code'] == 0:
            return ret['result']
        return []

    def fetch_pic_content(self, url, source_from):
        """

        :param url: -> string
        :param source_from: -> string
        :return: list
        """
        if url.find('http') < 0:
            host = self._host_map[source_from]
            url = host + url
        image_content = curl_common(url)
        return image_content

    def update_pic_content(self, picture_id, image_content):
        """

        :param picture_id: -> int
        :param image_content: -> byte
        :return: boolean
        """
        url = self._call_api_path
        method = 'add_picture_content'
        params = {
            'id': picture_id,
        }
        params_struct = {
            'method': method,
            'params': json.dumps(params),
        }
        response = curl_common(url, params=params_struct, body=image_content,
                               request_type=REQUEST_TYPE_POST)
        ret = json.loads(response)
        if 'result' in ret and ret['result'] is True:
            return ret['result']
        else:
            logging.info('error: ' + response)
        return False

    def add_image_detect(self, picture_id, image_content):
        """

        :param picture_id: -> int
        :param image_content: -> string
        :return: boolean
        """
        detect_result = self._fetch_image_detect(image_content)
        if detect_result is False:
            raise MyException('detect image failure')
        tmp_detect = detect_result['face_list'][0]
        url = self._call_api_path
        method = 'add_picture_detect'
        params = {
            'id': picture_id,
            'age': tmp_detect['age'],
            'beauty': tmp_detect['beauty'],
            'expression': tmp_detect['expression'],
            'face_shape': tmp_detect['face_shape'],
            'gender': 0,
            'glasses': tmp_detect['glasses'],
            'quality': tmp_detect['quality'],
            'other': tmp_detect,
        }
        if 'type' in tmp_detect['gender']:
            if tmp_detect['gender']['type'] == 'female':
                params['gender'] = SEX_MM
            else:
                params['gender'] = SEX_GG
        tmp_detect.pop('age')
        tmp_detect.pop('beauty')
        tmp_detect.pop('expression')
        tmp_detect.pop('face_shape')
        tmp_detect.pop('glasses')
        tmp_detect.pop('quality')
        tmp_detect.pop('gender')
        params_struct = {
            'method': method,
            'params': json.dumps(params),
        }
        response = curl_common(url, params=params_struct, request_type=REQUEST_TYPE_POST)
        ret = json.loads(response)
        if 'result' in ret and ret['result'] is True:
            return ret['result']
        else:
            logging.info('error: ' + response)
        return False

    def _fetch_image_detect(self, image_content):
        """

        :param image_content: -> string
        :return: dict
        """
        image = base64.b64encode(image_content)
        image_type = "BASE64"
        tmp_options = dict()
        tmp_options["face_field"] = "age,beauty,expression,faceshape,gender,glasses,landmark," \
                                    "race,quality,facetype"
        tmp_options["max_face_num"] = 2
        tmp_options["face_type"] = "LIVE"
        result = self._aip_client.detect(image, image_type, tmp_options)
        if result['error_code'] != 0:
            logging.info('code:%s, msg:%s' % (result['error_code'], result['error_msg']))
            return False

        return result['result']

    def _init_aip_client(self):
        self._aip_client = AipFace(self._aip_conf['app_id'], self._aip_conf['api_key'],
                                   self._aip_conf['secret_key'])


if __name__ == '__main__':
    pic_object = Picture()
    need_pic_list = pic_object.get_list()
    for row in need_pic_list:
        try:
            print "from: %s, url: %s" % (row['topic_from'], row['url'])
            tmp_content = pic_object.fetch_pic_content(url=row['url'],
                                                       source_from=row['topic_from'])
            res = pic_object.update_pic_content(picture_id=row['id'],
                                                image_content=tmp_content)
            pic_object.add_image_detect(picture_id=row['id'], image_content=tmp_content)
        except MyException as my_e:
            print my_e.message
            continue

    print "pic-length: %d" % (len(need_pic_list), )
