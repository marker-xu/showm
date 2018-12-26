# -*- coding: utf-8 -*-
from model.dao.topic import ModelDaoTopic, \
    ModelDaoPicture, \
    ModelDaoTopicStat, \
    ModelDaoPictureDetect
from lib.exception import BizException
from lib.util import *
from model.request.data import *
from model.response.data import *


class ModelDataTopic(object):

    _dao_topic = None
    _dao_picture = None
    _dao_stat = None
    _dao_pic_detect = None

    def __init__(self):
        self._dao_topic = ModelDaoTopic()
        self._dao_picture = ModelDaoPicture()
        self._dao_stat = ModelDaoTopicStat()
        self._dao_pic_detect = ModelDaoPictureDetect()

    def add_topic(self, request):
        """

        :param request: -> RequestAddTopic
        :return: -> ResponseAddTopic
        """
        topic_rows = self._dao_topic.get_topic(org_topic_id=request.org_topic_id,
                                               topic_from=request.topic_from)
        if topic_rows is not None:
            raise BizException('topic has exists')
        auto_id = self._dao_topic.add_topic(org_topic_id=request.org_topic_id,
                                            topic_from=request.topic_from,
                                            title=request.title, body=request.body,
                                            pic_list=[], sex=request.sex, qq=request.qq,
                                            weixin=request.weixin, email=request.email,
                                            author_name=request.author_name,
                                            author_id=request.author_id,
                                            author_homepage=request.author_homepage,
                                            post_time=request.post_time,
                                            topic_url=request.topic_url,
                                            board=request.board)

        self._dao_stat.add_stat(topic_id=auto_id,
                                org_topic_id=request.org_topic_id,
                                topic_from=request.topic_from,
                                popular_count=request.popular_count,
                                reply_count=request.reply_count)
        response = ResponseAddTopic()
        response.result = auto_id
        return response

    def get_topic(self, request):
        """

        :param request: -> RequestGetTopic
        :return: -> ResponseGetTopic
        """
        topic = self._dao_topic.get_topic(org_topic_id=request.org_topic_id,
                                          topic_from=request.topic_from)
        response = ResponseGetTopic()
        response.result = topic
        return response

    def get_topic_list(self, request):
        """

        :param request: -> RequestGetTopicList
        :return: ResponseGetTopicList
        """
        pass

    def add_pictures(self, request):
        """

        :param request: -> RequestAddPictures
        :return: -> boolean
        """
        topic_id = request.topic_id
        org_topic_id = request.org_topic_id
        topic_from = request.topic_from
        url_list = request.pic_list
        for url in url_list:
            self._dao_picture.add_picture(topic_id=topic_id, org_topic_id=org_topic_id,
                                          topic_from=topic_from, url=url, content="")
        response = ResponseAddPictures()
        response.result = True
        return response

    def add_picture_content(self, request):
        """

        :param request: -> RequestAddPictureContent
        :return: -> boolean
        """
        inc_id = request.id
        content = request.content
        rows = self._dao_picture.get_picture(inc_id)
        if rows is None:
            raise BizException('picture id not exists')
        pic_path = './static/pic/' + time_to_string(time.time(), "%Y%m%d")
        mk_dir(pic_path)
        file_name = pic_path + "/" + str(inc_id) + ".jpg"
        file_put_contents(file_name, content)
        res = self._dao_picture.update_picture_content(inc_id=inc_id, content=file_name)
        response = ResponseAddPictureContent()
        response.result = True
        if res < 1:
            response.result = False
        return response

    def get_picture_list(self, request):
        """

        :param request: -> RequestGetPictureList
        :return: list
        """
        rows = self._dao_picture.get_picture_list(topic_from=request.topic_from,
                                                  status=request.status,
                                                  offset=request.offset,
                                                  limit=request.limit)
        response = ResponseGetPictureList()
        response.result = rows
        return response

    def get_picture_total(self, request):
        """

        :param request: -> RequestGetPictureTotal
        :return: -> int
        """
        count = self._dao_picture.get_picture_total(topic_from=request.topic_from,
                                                    status=request.status)
        response = ResponseGetPictureTotal()
        response.result = count
        return response

    def update_stat(self, request):
        """

        :param request: -> RequestUpdateStat
        :return: -> ResponseUpdateStat
        """
        org_topic_id = request.org_topic_id
        topic_from = request.topic_from
        stat_row = self._dao_stat.get_stat(org_topic_id=org_topic_id,
                                           topic_from=topic_from)
        reply_count = request.reply_count
        popular_count = request.popular_count
        if stat_row is not None:
            self._dao_stat.update_stat_by_id(stat_id=stat_row['id'],
                                             popular_count=popular_count,
                                             reply_count=reply_count)
        else:
            topic = self._dao_topic.get_topic(org_topic_id=org_topic_id,
                                              topic_from=topic_from)
            self._dao_stat.add_stat(topic_id=topic['id'],
                                    org_topic_id=org_topic_id,
                                    topic_from=topic_from,
                                    popular_count=popular_count,
                                    reply_count=reply_count)
        response = ResponseUpdateStat()
        response.result = True
        return response

    def add_picture_detect(self, request):
        """

        :param request: -> RequestAddPictureDetect
        :return: -> ResponseAddPictureDetect
        """
        auto_id = self._dao_pic_detect.add_detect(picture_id=request.id, age=request.age,
                                                  beauty=request.beauty,
                                                  expression=request.expression,
                                                  face_shape=request.face_shape,
                                                  gender=request.gender,
                                                  glasses=request.glasses,
                                                  quality=request.quality,
                                                  other=request.other)
        response = ResponseAddPictureDetect()
        response.result = auto_id > 0
        return response


if __name__ == '__main__':
    print "kka"
