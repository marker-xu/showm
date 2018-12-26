# -*- coding: utf-8 -*-

import torndb
import time
import json
import logging
from model.dao.factory import get_db_inc


class ModelDaoTopic(object):
    """

    """
    _db = None
    _table_name = ""
    _basic_fields = []

    def __init__(self):
        self._db = get_db_inc()
        self._table_name = "show_topic"
        self._basic_fields = ["id", "org_topic_id", "topic_from", "title", "body",
                              "pic_list", "sex", "qq", "weixin", "email",
                              "author_name", "author_id", "author_homepage",
                              "post_time", "create_time", "topic_url"]

    def get_topic(self, org_topic_id, topic_from):
        sql = "SELECT " + ",".join(self._basic_fields) + " FROM " + self._table_name + " " \
              "WHERE org_topic_id=%s and topic_from=%s"
        rows = self._db.query(sql, org_topic_id, topic_from)
        if not rows:
            return None
        return rows[0]

    def add_topic(self, org_topic_id, topic_from, title, body, pic_list,
                  sex, qq, weixin, email, author_name, author_id,
                  author_homepage, post_time, topic_url, board):
        """

        :param org_topic_id: -> string
        :param topic_from: -> string
        :param title: -> string
        :param body: -> string
        :param pic_list: -> list
        :param sex: -> int
        :param qq: -> int
        :param weixin: -> string
        :param email: -> string
        :param author_name: -> string
        :param author_id: -> int
        :param author_homepage: -> string
        :param post_time: -> datetime
        :param topic_url: -> string
        :param board: -> string
        :return: -> int
        """
        sql = "INSERT INTO " + self._table_name + \
              " (org_topic_id, topic_from, title, body, pic_list, sex, qq, weixin," \
              " email, author_name, author_id, author_homepage, post_time," \
              " create_time, topic_url, board)" \
              " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        date_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        rows = [org_topic_id, topic_from, title, body, ",".join(pic_list), sex,
                int(qq), weixin, email, author_name, author_id,
                author_homepage, post_time, date_now, topic_url, board]
        logging.info('add_topic, sql-params: %s' % json.dumps(rows))
        auto_id = self._db.insert(sql, *rows)
        return auto_id

    def get_topic_list(self, topic_from=None, offset=None, limit=None):
        """

        :param topic_from: -> string
        :param offset: -> int
        :param limit: -> int
        :return:
        """
        sql = "SELECT " + ",".join(self._basic_fields) + " FROM " + self._table_name
        if topic_from is not None:
            sql = sql + " WHERE topic_from = '" + topic_from + "' "

        if limit is not None:
            sql = sql + " LIMIT %d, %d" % (offset, limit)

        rows = self._db.query(sql, topic_from)
        if not rows:
            return []
        return rows

    def get_topic_total(self, topic_from=None):
        """

        :param topic_from: -> string
        :return: -> int
        """
        sql = "SELECT COUNT(*) AS cc FROM " + self._table_name + " "
        if topic_from is not None:
            sql = sql + "WHERE topic_from = '" + topic_from + "' "
        rows = self._db.query(sql)
        if not rows:
            return 0
        else:
            return rows[0]['cc']


class ModelDaoPicture(object):
    _db = None
    _table_name = ""
    _basic_fields = []

    def __init__(self):
        self._db = get_db_inc()
        self._table_name = "show_topic_pic"
        self._basic_fields = ["id", "org_topic_id", "topic_from", "topic_id",
                              "url"]

    def add_picture(self, topic_id, org_topic_id, topic_from, url, content):
        """

        :param topic_id: -> int
        :param org_topic_id: -> string
        :param topic_from: -> string
        :param url: -> string
        :param content: -> string
        :return: -> int
        """
        sql_template = "INSERT INTO " + self._table_name + \
                       " (topic_id, org_topic_id, topic_from, url, content, create_time," \
                       " status)" \
                       " VALUES(%s, %s, %s, %s, %s, %s, 1)"
        date_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return self._db.insert(sql_template, topic_id, org_topic_id, topic_from, url,
                               content, date_now)

    def update_picture_content(self, inc_id, content):
        """
        更新内容
        :param inc_id: -> int
        :param content: -> string
        :return: -> int
        """
        date_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        sql_template = "UPDATE " + self._table_name + \
                       " SET content=%s, status =0, last_modified_time=%s WHERE id=%s"
        return self._db.update(sql_template, content, date_now, inc_id)

    def get_picture(self, inc_id):
        """
        获取图片内容
        :param inc_id: -> int
        :return: -> list
        """
        sql = "SELECT " + ",".join(self._basic_fields) + " FROM " + self._table_name + " WHERE id=%s"
        rows = self._db.query(sql, inc_id)
        if not rows:
            return None
        return rows[0]

    def get_picture_list(self, status=None, topic_from=None, offset=None, limit=None):
        """
        获取图片内容
        :param status -> int
        :param topic_from: -> string
        :param offset: -> int
        :param limit: -> int
        :return: -> list
        """
        sql = "SELECT " + ",".join(self._basic_fields) + " FROM " + self._table_name + \
              " WHERE 1"
        if topic_from is not None:
            sql = sql + " AND topic_from = '%s'" % (topic_from, )
        if status is not None:
            sql = sql + " AND status = %d" % (status, )
        if limit is not None:
            sql = sql + " LIMIT %d,%d" % (offset, limit)
        logging.info(sql)
        rows = self._db.query(sql)
        return rows

    def get_picture_total(self, status=None, topic_from=None):
        """
        获取图片数量
        :param status: -> int
        :param topic_from: -> string
        :return: -> int
        """
        sql = "SELECT COUNT(*) AS cc FROM " + self._table_name + " WHERE 1"
        if topic_from is not None:
            sql = sql + " AND topic_from = '" + topic_from + "' "
        if status is not None:
            sql = sql + " AND status = %d" % (status, )
        rows = self._db.query(sql)
        if not rows:
            return 0
        else:
            return rows[0]['cc']


class ModelDaoTopicStat(object):
    _db = None
    _table_name = ""
    _basic_fields = []

    def __init__(self):
        self._db = get_db_inc()
        self._table_name = "show_topic_stat"
        self._basic_fields = ["id", "org_topic_id", "topic_from", "topic_id",
                              "popular_count", "reply_count"]

    def get_stat(self, org_topic_id, topic_from):
        """

        :param org_topic_id: -> string
        :param topic_from: -> string
        :return: -> dict
        """
        sql = "SELECT " + ",".join(self._basic_fields) + " FROM " + \
              self._table_name + " WHERE org_topic_id=%s and topic_from=%s"
        rows = self._db.query(sql, org_topic_id, topic_from)
        if not rows:
            return None
        return rows[0]

    def add_stat(self, topic_id, org_topic_id, topic_from, reply_count, popular_count=0):
        """

        :param topic_id: -> int
        :param org_topic_id: -> string
        :param topic_from: -> string
        :param reply_count: -> int
        :param popular_count: -> int
        :return: -> int
        """
        sql_template = "INSERT INTO " + self._table_name + \
                       " (topic_id, org_topic_id, topic_from, reply_count," \
                       " popular_count, create_time)" \
                       " VALUES(%s, %s, %s, %s, %s, %s)"
        date_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return self._db.insert(sql_template, topic_id, org_topic_id, topic_from, reply_count,
                               popular_count, date_now)

    def update_stat_by_id(self, stat_id, reply_count, popular_count):
        """

        :param stat_id: -> int
        :param reply_count: -> int
        :param popular_count: -> int
        :return: -> int
        """
        sql_template = "UPDATE " + self._table_name + \
                       " SET reply_count=%s, popular_count=%s, last_modified_time=%s" \
                       " WHERE id=%s"
        date_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return self._db.update(sql_template, reply_count, popular_count, date_now, stat_id)


class ModelDaoPictureDetect(object):
    _db = None
    _table_name = ""
    _basic_fields = []

    def __init__(self):
        self._db = get_db_inc()
        self._table_name = "show_pic_detect"
        self._basic_fields = ["id", "picture_id", "age", "beauty", "expression", "face_shape", "gender",
                              "glasses", "quality", "other"]

    def add_detect(self, picture_id, age, beauty, expression, face_shape, gender, glasses,
                   quality, other):
        """

        :param picture_id: -> int
        :param age: -> int
        :param beauty: -> string
        :param expression: -> string
        :param face_shape: -> string
        :param gender: -> int
        :param glasses: -> string
        :param quality: -> string
        :param other: -> string
        :return: int
        """
        sql_template = "INSERT INTO " + self._table_name + \
                       " (picture_id, age, beauty, expression, face_shape, gender," \
                       " glasses, quality, other, create_time)" \
                       " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        date_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return self._db.insert(sql_template, picture_id, age, json.dumps(beauty),
                               json.dumps(expression), json.dumps(face_shape), gender,
                               json.dumps(glasses), json.dumps(quality), json.dumps(other),
                               date_now)

    def get_by_picture_id(self, picture_id):
        """
        更新内容
        :param picture_id: -> int
        :return: -> int
        """
        sql = "SELECT " + ",".join(self._basic_fields) + " FROM " + \
              self._table_name + " WHERE pic_id=%s"
        rows = self._db.query(sql, picture_id)
        if not rows:
            return None
        return rows[0]
