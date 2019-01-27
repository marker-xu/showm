# -*- coding: utf-8 -*-
import time, datetime
import requests
import re
import json
from lib.util import *

SEX_NONE = 0
SEX_GG = 1
SEX_MM = 2

# source
SOURCE_FUDAN = 'fudan'
SOURCE_SJTU = 'sjtu'
SOURCE_NJU = 'nju'
SOURCE_QINGHUA = 'newsmth'


class MyException(Exception):
    pass


def parse_sex(title):
    sex = SEX_NONE
    pattern = r'\[[^\]]+\][^\[]*\[([^\]]+)\]|【[^【]+】[^【]*【([^\]]+)】'
    p = re.compile(pattern=pattern, flags=re.I)
    tmp = p.findall(title)
    if len(tmp)>0:
        tmp_sex = tmp[0][0]
        if len(tmp[0][1])>0:
            tmp_sex = tmp[0][1]
        if tmp_sex == u'男':
            sex = SEX_GG
        elif tmp_sex == u'女':
            sex = SEX_MM
        return sex
    pattern = r'(%s|%s|mm|gg)' % (u'男', u'女')
    p = re.compile(pattern=pattern, flags=re.I)
    tmp = p.findall(title)
    if len(tmp) > 1:
        target = tmp[len(tmp)-1]
        if target == u'男' or target.lower() == 'gg' :
            sex = SEX_MM
        elif target == u'女' or target.lower() == 'mm':
            sex = SEX_GG
        return sex
    elif len(tmp) == 1:
        target = tmp[0]
        if target == u'男' or target.lower() == 'gg':
            sex = SEX_GG
        elif target == u'女' or target.lower() == 'mm':
            sex = SEX_MM
        return sex
    return sex


def parse_contact(topic_content):
    """
    获取联系方式
    :param topic_content:
    :return:
    """
    qq_pattern = r'qq[^\d]{0,5}([0-9]+)'
    qq_pattern2 = r'(%s|%s|%s)[^\d]{0,5}([0-9]+)' % ('扣扣', '球球', '求求')
    weixin_pattern = r'(weixin|wx|%s)[^\da-z\-\_]*([a-z0-9\_]+)' % ('微信', )
    email_pattern = r'[a-z\d][a-z\d\.\_\n]*@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}'
    result = {
        'qq': None,
        'weixin': None,
        'email': None
    }
    p = re.compile(pattern=qq_pattern, flags=re.I)
    tmp = p.findall(topic_content)
    if len(tmp) > 0:
        result['qq'] = tmp[0]
    else:
        p = re.compile(pattern=qq_pattern2, flags=re.I)
        tmp = p.findall(topic_content)
        if len(tmp) > 0:
            result['qq'] = tmp[0][1]
    p = re.compile(pattern=weixin_pattern, flags=re.I)
    tmp = p.findall(topic_content)
    if len(tmp) > 0:
        result['weixin'] = tmp[0][1]
    #print tmp
    p = re.compile(pattern=email_pattern, flags=re.I)
    tmp = p.findall(topic_content)
    if len(tmp) > 0:
        result['email'] = tmp[0].replace("\n", "")
    if result['qq'] is not None and result['email'] is None:
        result['email'] = result['qq'] + "@qq.com"
    return result


def parse_title(topic_content):
    """
    获取标题
    :param topic_content:
    :return:
    """
    pattern = r'%s\s*%s[\:：]+([^\n]+)\n' % ('标', '题')
    p = re.compile(pattern=pattern, flags=re.I)
    tmp = p.findall(topic_content)
    return tmp[0]


def parse_body(topic_content):
    """
    获取数据body
    :param topic_content:
    :return:
    """
    pattern = r'%s[\:：]+[^\n]+\n+([\S\s]+?)\n\n*[\-]*\n*\<\/font\>' % ('发信站', )
    p = re.compile(pattern=pattern, flags=re.I)
    tmp = p.findall(topic_content)
    return tmp[0]


def parse_picture(topic_content):
    """
    获取图片
    :param topic_content:
    :return:
    """
    pattern = r'<img\s*.*?src=\"*([^\s\"]+)\"*[^>]*>'
    p = re.compile(pattern=pattern, flags=re.I)
    tmp = p.findall(topic_content)
    pic_list = []
    if len(tmp) > 0:
        pic_list.extend(tmp)
    # 非常规图片或文档
    pattern = r'(http:\/\/[a-z\.\d]+(\/[a-z\-\_\.\d]+)*\/[a-z\-\_\.\d]+)'
    p = re.compile(pattern=pattern, flags=re.I)
    tmp = p.findall(topic_content)
    if len(tmp) > 0:
        for pic_tuple in tmp:
            pic_list.append(pic_tuple[0])
    #print pic_list
    return pic_list


class Topic(object):

    _call_api_path = ''

    def __init__(self):
        self._call_api_path = 'http://cp01-rdqa-dev005-xucongbin.epc.baidu.com:8494/api'

    def get_topic_list(self, board):
        pass

    def fetch_topic(self, dest_url):
        pass

    def add_topic(self, topic_left, topic_right):
        pass

    def add_pictures(self, real_topic_id, topic_id, pic_list):
        pass

    def parse_title(self, topic_content):
        pass

    def parse_body(self, topic_content):
        pass

    def check_topic_exists(self, topic_id):
        pass

    def update_stat(self, topic_id, reply_count, popular_count):
        pass

    def get_last_page(self, tmp_content):
        pass

    def gen_topic_url(self, dest_path):
        pass


if __name__ == '__main__':
    content = """
    [<a href='bbspst?board=LoveBridge&file=M.1542975539.A'>回复本文</a>]
    [<a href='bbscon?board=LoveBridge&file=M.1542975539.A'>原帖</a>] 发信人: 
    <a href="bbsqry?userid=Plinius">Plinius</a>(Plinius), 信区: LoveBridge
标  题: 【代挂】90MM真诚寻缘
发信站: 饮水思源 (2018年11月23日20:18:59 星期五)

同事MM，90年，安徽人，身高160，体重请看照片自行推测。上海二军医大硕士。感情经历
简单，大学期间谈过一次恋爱。毕业后从事知识产权行业有关工作，身边适龄单身男青年
不多，故一直单身至今。听说鹊桥板块相当靠谱，故勇敢在此挂牌，盼望能够觅得佳缘。
要求GG：
身高170以上，有涵养但不要太闷，幽默风趣健谈者加分，感情经历不要太丰富（四次恋爱
以上者减分）；
本科或以上学历，有正当职业，在上海工作生活；
对房、车无要求，但最好能担负得起首付；
家庭和睦，有责任感，以结婚为目的。
<IMG SRC="/file/LoveBridge/154297551381180.jpg" onload="if(this.width > screen.width - 200)
{this.width = screen.width - 200}"><br/>
<IMG SRC="/file/LoveBridge/154297552010471.jpg" onload="if(this.width > screen.width - 200)
{this.width = screen.width - 200}"><br/>
有意者请发送邮件至906687615qq.com，来信请附带照片及个人信息，谢谢！
--

</font><font class='c31'>※ 来源:·饮水思源 bbs.sjtu.edu.cn·[FROM: 180.170.72.83]</font>
<font class='c37'>
    """
    print parse_body(content)