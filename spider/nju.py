# -*- coding: utf-8 -*-
import time, datetime
import requests
import re
import json
import random
from lib.util import *
from model.topic import *


SOUTH_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                               'AppleWebKit/537.36 '
                               '(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                 'Host': 'bbs.nju.edu.cn',
                 'Upgrade-Insecure-Requests': '1',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                           'image/webp,image/apng,*/*;q=0.8',
                 'Referer': 'http://bbs.nju.edu.cn/bbstdoc?board=WarAndPeace'}

SOUTH_BASE_URL = 'http://bbs.nju.edu.cn'
SOURCE_FROM = SOURCE_NJU


class Nju(Topic):

    def get_topic_list(self, board, start=None):
        """
        <tr><td>3591<td><td><a href=bbsqry?userid=fanfan0706>fanfan0706</a><td>Oct 17 09:37
        <td><a href=bbstcon?board=WarAndPeace&file=M.1539740262.A>○ 代朋友发，89年女生诚征男友 </a>
        <td><font color=black>5</font>/<font color=red>3457</font>
        <tr><td>3592<td><td><a href=bbsqry?userid=aimifen>aimifen</a><td>Oct 17 10:45<td>
        <a href=bbstcon?board=WarAndPeace&file=M.1539744310.A>○ 代发，84年女征友 </a>
        <td><font color=black>4</font>/<font color=red>2602</font>
        <tr><td>3593<td><td><a href=bbsqry?userid=XQZS>XQZS</a><td>Oct 17 16:30
        <td><a href=bbstcon?board=WarAndPeace&file=M.1539765027.A>○ 大龄男征婚：从清明到重阳 </a><td>
        :param board: -> string
        :param start: -> int
        :return:
        """
        params = {'board': board}
        if start is not None:
            params['start'] = start
        dest_url = SOUTH_BASE_URL + "/bbstdoc"
        data = curl(dest_url, params, SOUTH_HEADERS)
        pattern = r'\<tr\><td>(\d+)\<td\>\<td\>\<a\s*href=([^\>]+)\>([^<]+)\<\/a\>' \
                  r'\<td\>([^<]+)\<td\>' \
                  r'\<a\s*href\=([^>]+)\>([^<]+)\<\/a\><td><font[^>]+>(\d+)\<\/font\>\/' \
                  r'<font[^>]+>(\d+)\<\/font\>'
        p = re.compile(pattern=pattern, flags=re.I)
        tmp = p.findall(data)
        result = []
        exclude_authors = ['deliver']
        for line in tmp:
            if line[2] in exclude_authors:
                continue
            if line[5].find("转载") >= 0 or line[5].find("撤牌") >= 0:
                continue
            result.append({
                'userId': line[0],
                'userUrl': line[1],
                'userName': line[2],
                'createTime': time_to_string(str_to_time("2018 " + line[3],
                                                         "%Y %b %d %H:%M")),
                'topicUrl': line[4],
                'topicTitle': line[5],
                'replyCount': line[6],
                'popularCount': line[7],
                'board': board,
                'topicId': line[4].replace('bbstcon?board=WarAndPeace&file=M.',
                                           '').replace('.A', ''),
            })
        return result

    def fetch_topic(self, dest_path):
        # bbstcon?board=WarAndPeace&file=M.1541319935.A
        url = self.gen_topic_url(dest_path)
        tmp_content = curl(url, headers=SOUTH_HEADERS)
        pattern = r'\<tr\>\<td\s*[^\s]+\s*id\=([^\>]+)\>[\s\n]+\<textarea[^\>]+\>' \
                  r'([\s\S]*?)\<\/textarea><\/table>'
        p = re.compile(pattern=pattern, flags=re.I)
        #print tmp_content
        tmp = p.findall(tmp_content)
        topic_body = tmp[0][1]

        result = {
            'topicId': dest_path.replace('bbstcon?board=WarAndPeace&file=M.',
                                         '').replace('.A', ''),
            'contact': parse_contact(topic_body),
            'body': self.parse_body(topic_body),
            'title': self.parse_title(topic_body),
            'picList': parse_picture(topic_body)
        }
        #print result
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
        """
        获取数据body
        :param topic_content:
        :return:
        """
        pattern = r'%s[\:：]+[^\n]+\n+([\S\s]+?)\n\n*\-\-*' % ('发信站', )
        p = re.compile(pattern=pattern, flags=re.I)
        tmp = p.findall(topic_content)
        return tmp[0]

    def add_topic(self, topic_left, topic_right):
        url = self._call_api_path
        method = 'add_topic'
        params = {
            'topic_id': topic_right['topicId'],
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
            'popular_count': topic_left['popularCount'],
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
        params = {'board': board}
        if start is not None:
            params['start'] = start
        dest_url = SOUTH_BASE_URL + "/bbstdoc"
        tmp_content = curl(dest_url, params, SOUTH_HEADERS)
        pattern = '<a\s*href\=([^\>]+)\>%s</a>' % ('上一页', )
        p = re.compile(pattern=pattern, flags=re.I)
        #print tmp_content
        tmp = p.findall(tmp_content)
        return tmp[0]

    def gen_topic_url(self, dest_path):
        return SOUTH_BASE_URL + '/' + dest_path


if __name__ == '__main__':

    nju_topic = Nju()
    tmp_board = 'WarAndPeace'
    tmp_start = None
    org_topic_list = nju_topic.get_topic_list(board=tmp_board, start=tmp_start)
    print "init-topic-length: %d" % (len(org_topic_list), )
    print "last-page: %s" %(nju_topic.get_last_page(board=tmp_board, start=tmp_start))
    topic_list = []
    for topic in org_topic_list:
        tmp_topic_id = topic['topicId']
        print "title:%s, url:%s" % (topic['topicTitle'],
                                    nju_topic.gen_topic_url(topic['topicUrl']), )
        if nju_topic.check_topic_exists(tmp_topic_id) is True:
            print "topic%s has exists" % (tmp_topic_id, )
            nju_topic.update_stat(topic_id=tmp_topic_id,
                                  reply_count=topic['replyCount'],
                                  popular_count=topic['popularCount'])
            continue
        try:
            topic_struct = nju_topic.fetch_topic(topic['topicUrl'])

            topic_list.append(topic_struct)
            print len(topic_struct['body'])
            nju_topic.add_topic(topic, topic_struct)
            time.sleep(2)
        except MyException as my_e:
            print my_e.message
            continue

    print len(topic_list)
    #print topic_list
