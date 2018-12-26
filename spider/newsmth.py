# -*- coding: utf-8 -*-
import time, datetime
import requests
import re
import json
import random
from lib.util import *
from model.topic import *


SOUTH_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 '
                               'Safari/537.36',
                 'Host': 'www.newsmth.net',
                 'Upgrade-Insecure-Requests': '1',
                 'Cookie': 'main[UTMPUSERID]=guest; main[UTMPKEY]=20949697; main[UTMPNUM]=15233; '
                           'Hm_lvt_bbac0322e6ee13093f98d5c4b5a10912=1544317497; '
                           'Hm_lpvt_bbac0322e6ee13093f98d5c4b5a10912=1544319316',
                 'Accept': '*/*',
                 'Referer': 'http://www.newsmth.net/nForum/'}

SOUTH_BASE_URL = 'http://www.newsmth.net'
SOURCE_FROM = SOURCE_QINGHUA


class Qinghua(Topic):

    _pattern_post_time = r'%s[\:：][^(]+\(([^\)]+)\)[^\<]+' % ('发信站', )

    def get_topic_list(self, board, start=None):
        """
        <tr><td>3591<td><td><a href=bbsqry?userid=fanfan0706>fanfan0706</a><td>Oct 17 09:37<td>
        <a href=bbstcon?board=WarAndPeace&file=M.1539740262.A>○ 代朋友发，89年女生诚征男友 </a>
        <td><font color=black>5</font>/<font color=red>3457</font>
        <tr><td>3592<td><td><a href=bbsqry?userid=aimifen>aimifen</a><td>Oct 17 10:45<td>
        <a href=bbstcon?board=WarAndPeace&file=M.1539744310.A>○ 代发，84年女征友 </a>
        <td><font color=black>4</font>/<font color=red>2602</font>
        <tr><td>3593<td><td><a href=bbsqry?userid=XQZS>XQZS</a><td>Oct 17 16:30<td>
        <a href=bbstcon?board=WarAndPeace&file=M.1539765027.A>○ 大龄男征婚：从清明到重阳 </a><td>
        :param board: -> string
        :param start: -> int
        :return:
        """
        params = {'ajax': 1}
        if start is not None:
            params['p'] = start
        dest_url = SOUTH_BASE_URL + "/nForum/board/" + board + "?ajax"
        data = curl(dest_url, params, SOUTH_HEADERS)
        pattern = r'\<tr\s>' \
                  r'\<td[^\>]+>\<a[^\>]+\>\<samp[^\>]+\>\s*<\/samp\><\/a\>\<\/td\>' \
                  r'\<td[^\>]+\>\<a\s*href=\"([^\"\>]+)\"\>([^\<]+)\<\/a\>.*?\<\/td\>' \
                  r'\<td[^\>]+>([^\<]+)\<\/td\>' \
                  r'\<td[^\>]+\>[^\<]+\<a\s*href=\"([^\"\>]+)\"[^\>]*\>([^\<]+)\<\/a\>\<\/td\>' \
                  r'\<td[^\>]+>.*?\<\/td\>' \
                  r'\<td[^\>]+>(\d*)\<\/td\>' \
                  r'\<td[^\>]+>([^\<]+)\<\/td\>' \
                  r'\<td[^\>]+>.*?\<\/td\>' \
                  r'\<td[^\>]+>.*?\<\/td\>' \
                  r'\<\/tr\>'
        p = re.compile(pattern=pattern, flags=re.I)
        tmp = p.findall(data)
        result = []
        exclude_authors = ['deliver']
        for line in tmp:
            if line[3] in exclude_authors:
                continue
            if line[1].find("Re:") >= 0 or line[1].find("撤牌") >= 0:
                continue
            popular_count = 0
            if len(line[5]) > 0:
                popular_count = int(line[5])
            result.append({
                'userId': 0,
                'userUrl': line[3],
                'userName': line[4],
                'topicUrl': line[0],
                'topicTitle': line[1],
                'topicId': line[0].replace('/nForum/article/PieLove/', ''),
                'replyCount': int(line[6]),
                'popularCount': popular_count,
                'board': board,
            })
        return result

    def fetch_topic(self, dest_path):
        # bbstcon?board=WarAndPeace&file=M.1541319935.A
        url = SOUTH_BASE_URL + dest_path + '?ajax'
        print url
        tmp_content = curl(url, headers=SOUTH_HEADERS)
        pattern = r'\<td\s*class\=\"a-content\"\><p\s>' \
                  r'(.*?)\<\/p>.*?<\/td>\<\/tr\>'
        p = re.compile(pattern=pattern, flags=re.I)
        tmp = p.findall(tmp_content)
        topic_body = tmp[0].replace('&nbsp;', ' ')

        result = {
            'contact': parse_contact(topic_body),
            'body': self.parse_body(topic_body),
            'picList': parse_picture(topic_body),
            'createTime': self.parse_post_time(topic_body),
        }
        result['createTime'] = time_to_string(str_to_time(result['createTime'],
                                                          '%a %b %d %H:%M:%S %Y'))
        if len(tmp) > 1:
            pic1 = parse_picture(tmp[1][1])
            if len(pic1) > 0:
                result['picList'].extend(pic1)
        if len(tmp) > 2:
            pic2 = parse_picture(tmp[2][1])
            if len(pic2) > 0:
                result['picList'].extend(pic2)
        if len(result['picList']) > 0:
            result['picList'] = [x.replace('//att.newsmth.net', '') for x in result['picList']]
            print result['picList']
        return result

    def parse_title(self, topic_content):
        return parse_title(topic_content)

    def parse_body(self, topic_content):
        """
        获取数据body
        :param topic_content:
        :return:
        """
        pattern = r'%s[\:：][^\<]+\<br\s\/\>\s*\<br\s\/\>\s*' \
                  r'(.*?)' \
                  r'\s*\<br\s\/\>\s*\<font\s*class=\"f[\d]+\"\>' % ('发信站', )
        p = re.compile(pattern=pattern, flags=re.I)
        tmp = p.findall(topic_content)
        if len(tmp) > 0:
            return tmp[0]
        print topic_content
        pattern = r'%s[\:：][^\<]+(\<font\s*class=\"f[\d]+\"\>[^\<]+\<\/font\>)*' \
                  r'\<font\s*class=\"f[\d]+\"\>\s*\<br\s\/\>\s*\<br\s\/\>\s*' \
                  r'(.*?)' \
                  r'\s*\<br\s\/\>\s*<\/font>\<font\s*class=\"f[\d]+\"\>' % ('发信站', )
        p = re.compile(pattern=pattern, flags=re.I)
        tmp = p.findall(topic_content)
        return tmp[0][1]

    def parse_post_time(self, topic_content):
        """
        获取数据body
        :param topic_content:
        :return:
        """
        pattern = self._pattern_post_time
        p = re.compile(pattern=pattern, flags=re.I)
        tmp = p.findall(topic_content)
        return tmp[0]

    def add_topic(self, topic_left, topic_right):
        url = self._call_api_path
        method = 'add_topic'
        params = {
            'topic_id': topic_left['topicId'],
            'topic_url': topic_left['topicUrl'],
            'title': topic_left['topicTitle'],
            'body': topic_right['body'],
            'contact': topic_right['contact'],
            'author_id': topic_left['userId'],
            'author_name': topic_left['userName'],
            'author_homepage': topic_left['userUrl'],
            'create_time': topic_right['createTime'],
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
        params = {'ajax': 1}
        if start is not None:
            params['p'] = start
        dest_url = SOUTH_BASE_URL + "/nForum/board/" + board + "?ajax"
        tmp_content = curl(dest_url, params, SOUTH_HEADERS)
        pattern = '<a\s*href\=\"([^\"]+)\"\s*title=\"%s\"\>\>\></a>' % ('下一页', )
        p = re.compile(pattern=pattern, flags=re.I)
        #print tmp_content
        tmp = p.findall(tmp_content)
        return tmp[0]


if __name__ == '__main__':

    qinghua_topic = Qinghua()
    tmp_board = 'PieLove'
    tmp_start = None
    org_topic_list = qinghua_topic.get_topic_list(board=tmp_board, start=tmp_start)
    print "init-topic-length: %d" % (len(org_topic_list), )
    print "last-page: %s" % (qinghua_topic.get_last_page(board=tmp_board, start=tmp_start))
    topic_list = []
    for topic in org_topic_list:
        tmp_topic_id = topic['topicId']
        if qinghua_topic.check_topic_exists(tmp_topic_id) is True:
            print "topic:%s has exists" % (tmp_topic_id, )
            qinghua_topic.update_stat(topic_id=tmp_topic_id,
                                      reply_count=topic['replyCount'],
                                      popular_count=topic['popularCount'])
            continue
        try:
            topic_struct = qinghua_topic.fetch_topic(topic['topicUrl'])
            if len(topic_struct['body'].decode('utf8')) > 4096:
                print "topic:%s, title:%s length is large" % (tmp_topic_id,
                                                              topic['topicTitle'], )
                continue
            topic_list.append(topic_struct)
            print len(topic_struct['body'])
            qinghua_topic.add_topic(topic, topic_struct)
            time.sleep(2)
        except MyException as my_e:
            print my_e.message
            continue

    print len(topic_list)
    #print topic_list
