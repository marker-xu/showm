# -*- coding: utf-8 -*-
import time, datetime
import requests
import re
import json
from lib.util import *
from model.topic import *


SOUTH_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                               'AppleWebKit/537.36 '
                               '(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                 'Host': 'bbs.sjtu.edu.cn',
                 'Upgrade-Insecure-Requests': '1',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
                           'image/apng,*/*;q=0.8',
                 'Referer': 'https://bbs.sjtu.edu.cn/bbsdoc?board=LoveBridge'}

SOUTH_BASE_URL = 'https://bbs.sjtu.edu.cn'
SOURCE_FROM = SOURCE_SJTU


class Sjtu(Topic):

    def get_topic_list(self, board, start=None):
        """
        <tr><td>5932<td><td><a href="bbsqry?userid=tiffanyy">tiffanyy</a><td>Oct 27 17:38
        <td><a href=bbstcon,board,LoveBridge,reid,1540633121.html>○ 88江苏MM双11前一挂 </a>(1回复)
        <tr><td>5933<td><td><a href="bbsqry?userid=shangrila">shangrila</a>
        <td>Oct 27 20:23<td><a href=bbstcon,board,LoveBridge,reid,1540642992.html>
        ○ 【代挂】【女】89年MM真诚征友，非诚勿扰 </a>(0回复)
        <tr><td>5934<td>M<td><a href="bbsqry?userid=privia">privia</a><td>Oct 27 20:47
        <td><a href=bbstcon,board,LoveBridge,reid,1540644424.html>
        ○ [代挂][男][pic]93年爱篮球180阳光男生诚征好友 </a>(0回复)
        :return:
        """
        dest_url = SOUTH_BASE_URL + "/bbstdoc,board," + board + "%s.html"
        temp_page = ""
        if start is not None:
            temp_page = ",page," + str(start)
        dest_url = dest_url % (temp_page, )
        data = curl(dest_url, None, SOUTH_HEADERS)
        #file_put_contents('./sjtu-list.txt', data)
        #data = file_get_contents('./sjtu-list.txt')
        pattern = r'\<tr\><td>(\d+)\<td\>\<td\>' \
                  r'\<a\s*href=\"*([^\>\"]+)\"*\>([^<]+)\<\/a\>' \
                  r'\<td\>([^<]+)\<td\>' \
                  r'\<a\s*href\=\"*([^>\"]+)\"*\>([^<]+)\<\/a\>\((\d+)[^\)]+\)'
        p = re.compile(pattern=pattern, flags=re.I)
        tmp = p.findall(data)
        result = []
        for line in tmp:
            if line[2] == 'SJTUBBS' or line[5].find('撤牌') >= 0:
                continue
            result.append({
                'userId': line[0],
                'userUrl': line[1],
                'userName': line[2],
                'createTime': time_to_string(str_to_time("2019 " + line[3],
                                                         "%Y %b %d %H:%M")),
                'topicUrl': line[4],
                'topicTitle': line[5],
                'topicId': line[4].replace('bbstcon,board,LoveBridge,reid,',
                                           '').replace('.html', ''),
                'replyCount': line[6],
                'board': board,
            })
        return result

    def fetch_topic(self, dest_path):
        url = SOUTH_BASE_URL + '/' + dest_path
        print url
        tmp_content = curl(url, headers=SOUTH_HEADERS)
        pattern = r'\<tr\>\<td[^\>]*\>\s*<pre[^\>]*\>([\s\S]*?)\<\/pre><\/table>'
        p = re.compile(pattern=pattern, flags=re.I)
        #print tmp_content
        tmp = p.findall(tmp_content)
        #print tmp
        topic_body = tmp[0]

        result = {
            'topicId': (dest_path.replace('bbstcon,board,LoveBridge,reid,',
                                          '').replace('.html', '')),
            'contact': parse_contact(topic_body),
            'body': self.parse_body(topic_body),
            'title': self.parse_title(topic_body),
            'picList': parse_picture(topic_body)
        }
        #print parse_body(topic_body)
        if len(tmp) > 1:
            pic1 = parse_picture(tmp[1][1])
            if len(pic1) > 0:
                result['picList'].extend(pic1)
        if len(tmp) > 2:
            pic2 = parse_picture(tmp[2][1])
            if len(pic2) > 0:
                result['picList'].extend(pic2)
        return result

    def parse_title(self, topic_content):
        return parse_title(topic_content)

    def parse_body(self, topic_content):
        return parse_body(topic_content)

    def check_topic_exists(self, topic_id):
        url = self._call_api_path
        method = 'check_topic_exists'
        params = {
            'topic_id': topic_id,
            'topic_from': SOURCE_FROM,
        }
        params_struct = {
            'method': method,
            'params': json.dumps(params),
        }
        response = curl_common(url, params=params_struct)
        ret = json.loads(response)
        if 'result' in ret and ret['result'] is True:
            return True
        return False

    def add_topic(self, topic_left, topic_right):
        url = self._call_api_path
        method = 'add_topic'
        params = {
            'topic_id': (topic_right['topicId']),
            'topic_url': topic_left['topicUrl'],
            'title': topic_left['topicTitle'],
            'body': topic_right['body'],
            'contact': topic_right['contact'],
            'author_id': topic_left['userId'],
            'author_name': topic_left['userName'],
            'author_homepage': topic_left['userUrl'],
            'create_time': topic_left['createTime'],
            'topic_from': SOURCE_FROM,
            'sex': parse_sex(topic_left['topicTitle'].decode('utf8')),
            'board': topic_left['board'],
            'reply_count': topic_left['replyCount'],
            'popular_count': 0,
        }
        params_struct = {
            'method': method,
            'params': json.dumps(params),
        }
        response = curl_common(url, params=params_struct)
        ret = json.loads(response)
        if ret['code'] != 0:
            logging.info('error: ' + ret['message'], ret)
            raise MyException(ret['message'])
        auto_id = ret['result']
        self.add_pictures(auto_id, params['topic_id'], topic_right['picList'])

    def add_pictures(self, real_topic_id, topic_id, pic_list):
        if len(pic_list) == 0:
            return True
        url = self._call_api_path
        method = 'add_pictures'
        params = {
            'id': real_topic_id,
            'topic_id': topic_id,
            'topic_from': SOURCE_FROM,
            'pic_list': pic_list
        }
        params_struct = {
            'method': method,
            'params': json.dumps(params),
        }
        response = curl_common(url, params=params_struct)
        ret = json.loads(response)
        if 'result' in ret and ret['result'] is True:
            return True
        return False

    def update_stat(self, topic_id, reply_count, popular_count):
        url = self._call_api_path
        method = 'update_stat'
        params = {
            'topic_id': topic_id,
            'topic_from': SOURCE_FROM,
            'reply_count': reply_count,
            'popular_count': popular_count,
        }
        params_struct = {
            'method': method,
            'params': json.dumps(params),
        }
        response = curl_common(url, params=params_struct)
        ret = json.loads(response)
        if 'result' in ret and ret['result'] is True:
            return True
        return False

    def get_last_page(self, board, start=None):
        """

        :param board: -> string
        :param start: -> int
        :return: -> string
        """
        dest_url = SOUTH_BASE_URL + "/bbstdoc,board," + board + "%s.html"
        temp_page = ""
        if start is not None:
            temp_page = ",page," + str(start)
        dest_url = dest_url % (temp_page, )
        tmp_content = curl(dest_url, None, SOUTH_HEADERS)
        pattern = '<a\s*href\=([^\>]+)\>%s</a>' % ('上一页', )
        p = re.compile(pattern=pattern, flags=re.I)
        #print tmp_content
        tmp = p.findall(tmp_content)
        return tmp[0]

    def gen_topic_url(self, dest_path):
        return SOUTH_BASE_URL + '/' + dest_path


if __name__ == '__main__':

    sjtu_topic = Sjtu()
    tmp_board = 'LoveBridge'
    tmp_start = None
    org_topic_list = sjtu_topic.get_topic_list(board=tmp_board, start=tmp_start)
    print "init-topic-length: %d" % (len(org_topic_list), )
    print "last-page: %s" %(sjtu_topic.get_last_page(board=tmp_board, start=tmp_start))
    topic_list = []
    for topic in org_topic_list:
        try:
            tmp_topic_id = topic['topicId']
            print "title:%s, url:%s" % (topic['topicTitle'],
                                        sjtu_topic.gen_topic_url(topic['topicUrl']), )
            if sjtu_topic.check_topic_exists(tmp_topic_id) is True:
                print "topic%s has exists" % (tmp_topic_id, )
                sjtu_topic.update_stat(topic_id=tmp_topic_id,
                                       reply_count=topic['replyCount'],
                                       popular_count=0)
                continue
            topic_struct = sjtu_topic.fetch_topic(topic['topicUrl'])
            topic_list.append(topic_struct)
            #print topic_struct
            sjtu_topic.add_topic(topic, topic_struct)
            time.sleep(1)
        except MyException as my_e:
            print my_e.message
            continue

    print len(topic_list)
    #print topic_list
