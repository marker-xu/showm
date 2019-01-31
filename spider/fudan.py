# -*- coding: utf-8 -*-
import time, datetime
import requests
import re
import json
import logging
from xml.etree import ElementTree as XmlEt
from lib.util import *
from model.topic import *


SOUTH_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                               'AppleWebKit/537.36' +
                               ' (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                 'Host': 'bbs.fudan.sh.cn',
                 'Upgrade-Insecure-Requests': '1',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
                           'image/apng,*/*;q=0.8',
                 'Referer': 'https://bbs.fudan.sh.cn/v18/doc?bid=120'}

SOUTH_BASE_URL = 'https://bbs.fudan.sh.cn'
SOURCE_FROM = SOURCE_FUDAN


class Fudan(Topic):

    board_dict = {
        'Single': 120,
        'Magpie_Bridge': 70,
    }

    def get_topic_list(self, board, start=None):
        """
        <?xml version="1.0" encoding="utf-8"?>
        <?xml-stylesheet type="text/xsl" href="../xsl/beta.xsl?v20150923"?>
        <bbsdoc><session m='t'><p>    </p><u></u><f><b bid='213'>House</b><b bid='90'>Emprise</b>
        <b bid='94'>Poetry</b><b bid='110'>Employees</b><b bid='217'>Auto</b>
        <b bid='45'>MobilePhone</b></f></session>
        <po m='N' owner='deliver' time= '2018-09-10T20:05:02' id='3222444133266228835'>
        恢复DavidHao在Single版的发文权限</po>
        <po m='N' owner='deliver' time= '2018-09-10T20:05:10' id='3222444149611431529'>
        恢复RafaelZhou在Single版的发文权限</po>
        <po nore='1' m='M' owner='arkchen' time= '2018-09-14T09:58:47' id='3223092623304557539'>
        （代友发）89MM真诚寻小哥哥（附照片）</po>
        <po nore='1' m='G' owner='justit' time= '2018-09-19T13:15:39' id='3224023364655907521'>
        93复旦男寻女友，无pic</po>
        <po m='N' owner='xQi' time= '2018-09-26T13:37:44' id='3225294500635083788'>
        [合集]中秋真诚一挂</po>
        <po sticky='1' nore='1' m='M' owner='mm' time= '2013-12-14T13:56:19' id='2908751038934681202'>
        Single版版规公示</po>
        <po sticky='1' m='N' owner='cccyo' time= '2011-09-24T00:10:19' id='2761517630350164687'>
        建议本版挂牌者慎重选用个人主邮箱</po>
        <brd title='Single' desc='网络光协' bm='xQi' total='5255' start='5236' bid='120' page='20'
        link='t' anony='0' attach='307200' banner='../info/boards/Single/banner.jpg'/>
        </bbsdoc>
        :
        :param board: -> string
        :param start: -> int
        :return:
        """
        params = {'board': board}
        if start is not None:
            params['start'] = start
        print params
        dest_url = SOUTH_BASE_URL + "/v18/doc"
        data = curl(dest_url, params, SOUTH_HEADERS, 'utf8')
        #file_put_contents('./fudan_list.txt', data)
        topic_url_prefix = 'v18/tcon?new=1&bid=' + str(self.board_dict[board]) + '&f='
        result = []
        root = XmlEt.fromstring(data.strip())
        for child in root.findall("po[@nore='1']"):
            if child.text.find('Re') >= 0 or 'sticky' in child.attrib:
                continue
            if child.text.find(u"转载") >= 0 or child.text.find(u"撤牌") >= 0:
                continue
            sex = 0
            if child.attrib['m'].lower() == 'g':
                sex = 1
            elif child.attrib['m'].lower() == 'm':
                sex = 2

            result.append({
                'userId': 0,
                'userUrl': 'v18/qry?u=' + child.attrib['owner'],
                'userName': child.attrib['owner'],
                'topicId': child.attrib['id'],
                'createTime': child.attrib['time'].replace('T', " "),
                'topicUrl': topic_url_prefix + child.attrib['id'],
                'topicTitle': child.text,
                'sex': sex,
                'board': board,
            })
        return result

    def fetch_topic(self, dest_path):
        """
        <?xml version="1.0" encoding="utf-8"?>
    <?xml-stylesheet type="text/xsl" href="../xsl/beta.xsl?v20150923"?>
    <bbstcon bid='120' bname='Single' gid='3233785008602744064' anony='0' page='20'
    attach='307200' last='1'><session m='t'><p>    </p><u></u><f><b bid='213'>House</b>
    <b bid='90'>Emprise</b><b bid='94'>Poetry</b><b bid='110'>Employees</b><b bid='217'>Auto</b>
    <b bid='45'>MobilePhone</b></f></session>
    <po fid='3233785008602744064' owner='sherrillzxy'>
    <owner>sherrillzxy</owner>
    <nick>sherrill</nick>
    <board>Single</board>
    <title>93年海归妹子诚意挂牌</title>
    <date>2018年11月12日10:14:13 星期一</date>
    <pa m='t'>
    <p>帮同事妹子挂牌，欢迎靠谱男生诚意摘牌~</p>
    <p><br/></p>
    <p>93年海归妹子在沪诚招男友:</p>
    <p>妹子是一名93年的海归，原籍为浙江宁波。现居上海，已落上海户口。</p>
    <p>在美国西海岸念的本科，学校名列前茅。熟悉美国东西两岸。在美国工作后回到上海，从事金融风险管理的工作。
    平时生活简单，喜欢看电影，游泳，旅游。喜欢搜寻好吃的食物，看没看过的展览。心态积极乐观，性格阳光开朗。</p>
    <p>希望另一半为江浙沪人士，现居上海。有正当工作，长相干净，身高172cm以上，有良好的家庭教养，三观相符。
    如果你是我需要等的人，那么请发邮件简单介绍一下自己吧。我的邮箱是sandy66668888@sina.com。</p>
    <p>非诚勿扰哦。是对的人那么等久一点又何妨你说是吧？</p>
    <p><br/></p>
    <p><br/></p>
    <p><a i='i' href='http://bbs.fudan.edu.cn/upload/Single/1541988812-9595.jpg'/></p>
    <p><br/></p>
    <p><a i='i' href='http://bbs.fudan.edu.cn/upload/Single/1541988825-7854.jpg'/></p>
    <p><br/></p>
    </pa>
    <pa m='s'>
    <p>--</p>
    <p><c h='0' f='37' b='40'></c><c h='1' f='34' b='40'>※ 来源:·日月光华 bbs.fudan.edu.cn·HTTP
    [FROM: 101.81.237.*]</c><c h='0' f='37' b='40'></c></p>
    </pa>
    </po>
    </bbstcon>
        :param dest_path:
        :return:
        """
        url = self.gen_topic_url(dest_path=dest_path)
        topic_body = ""
        tmp_content = curl(url, headers=SOUTH_HEADERS, encoding='utf8')
        root = XmlEt.fromstring(tmp_content)
        index = 1
        result = {}
        tmp = []
        for child in root.iter("po"):
            if index == 1:
                topic_body = XmlEt.tostring(child.find("pa[@m='t']"), encoding="utf8", method="html")
                result['userNick'] = child.find("nick").text
                result['title'] = child.find("title").text
            else:
                tmp.append(XmlEt.tostring(child.find("pa[@m='t']"), encoding="utf8", method="html"))
            index = index + 1
        #print len(tmp)
        #print topic_body
        result['body'] = topic_body
        result['replyCount'] = len(tmp)
        result['picList'] = parse_picture(topic_body)
        result['contact'] = parse_contact(topic_body)
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
            'create_time': topic_left['createTime'],
            'topic_from': SOURCE_FROM,
            'sex': topic_left['sex'],
            'board': topic_left['board'],
            'reply_count': topic_right['replyCount'],
            'popular_count': 0,
        }
        if params['sex'] == SEX_NONE:
            print params['title']
            params['sex'] = parse_sex(params['title'])
            print params['sex']
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

    def check_topic_exists(self, topic_id, board):
        url = self._call_api_path
        method = 'check_topic_exists'
        params = {
            'topic_id': topic_id,
            'topic_from': SOURCE_FROM,
            'board': board,
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

    def gen_topic_url(self, dest_path):
        return SOUTH_BASE_URL + '/' + dest_path


if __name__ == '__main__':

    fudan_topic = Fudan()
    tmp_board = 'Single'
    org_topic_list = fudan_topic.get_topic_list(tmp_board)
    #print org_topic_list
    topic_list = []
    for topic in org_topic_list:
        try:
            print "title:%s, url:%s" % (topic['topicTitle'],
                                        fudan_topic.gen_topic_url(topic['topicUrl']), )
            topic_struct = fudan_topic.fetch_topic(topic['topicUrl'])
            topic_list.append(topic_struct)
            fudan_topic.add_topic(topic, topic_struct)
            tmp_topic_id = topic['topicId']
            fudan_topic.update_stat(topic_id=tmp_topic_id,
                                    reply_count=topic_struct['replyCount'],
                                    popular_count=0)
            time.sleep(1)
        except MyException as my_e:
            print my_e.message
            continue
        #break
    #Magpie_Bridge
    tmp_board = 'Magpie_Bridge'
    print tmp_board
    org_topic_list = fudan_topic.get_topic_list(tmp_board)
    #print org_topic_list
    topic_list = []
    for topic in org_topic_list:
        try:
            print "title:%s, url:%s" % (topic['topicTitle'],
                                                        fudan_topic.gen_topic_url(topic['topicUrl']), )
            topic_struct = fudan_topic.fetch_topic(topic['topicUrl'])
            topic_list.append(topic_struct)
            #print topic_struct
            fudan_topic.add_topic(topic, topic_struct)
            tmp_topic_id = topic['topicId']
            fudan_topic.update_stat(topic_id=tmp_topic_id,
                                    reply_count=topic_struct['replyCount'],
                                    popular_count=0)
            time.sleep(1)
        except MyException as my_e:
            print my_e.message
            continue
    print len(topic_list)
