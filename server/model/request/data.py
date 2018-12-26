# -*- coding: utf-8 -*-


class RequestBase(object):

    _allow_keys = []
    _format_rules = {}

    def __setattr__(self, key, value):
        if key not in self._allow_keys:
            return False
        self.__dict__[key] = value

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        elif key in self._allow_keys:
            return None
        else:
            msg = "object has no attribute %s" % (key, )
            raise AttributeError(msg)

    def make_request(self, params):
        """

        :param params: -> dict
        :return: -> None
        """
        self._format(params)
        for key in self._allow_keys:
            if key in params:
                self.__setattr__(key, params[key])

    def _format(self, params):
        for key in self._allow_keys:
            if key not in self._format_rules or key not in params:
                continue
            rule = self._format_rules[key]
            if rule == 'int':
                params[key] = int(params[key])
            elif rule == 'trim':
                params[key] = params[key].strip()
            elif rule == 'float':
                params[key] = float(params[key])


class RequestAddTopic(RequestBase):
    _allow_keys = ['org_topic_id', 'topic_from', 'title', 'body', 'pic_list', 'sex', 'qq',
                   'weixin', 'email', 'author_name', 'author_id', 'author_homepage',
                   'post_time', 'topic_url', 'board', 'reply_count', 'popular_count']

    _format_rules = {'org_topic_id': 'trim', }


class RequestGetTopicList(RequestBase):
    _allow_keys = ['topic_from', 'offset', 'limit']


class RequestGetTopic(RequestBase):
    _allow_keys = ['org_topic_id', 'topic_from']


class RequestAddPictures(RequestBase):
    _allow_keys = ['topic_id', 'org_topic_id', 'topic_from', 'pic_list']


class RequestAddPictureContent(RequestBase):
    _allow_keys = ['id', 'content']


class RequestGetPictureList(RequestBase):
    _allow_keys = ['status', 'topic_from', 'offset', 'limit']
    _format_rules = {'status': 'int', 'offset': 'int', 'limit': 'int'}


class RequestGetPictureTotal(RequestBase):
    _allow_keys = ['status', 'topic_from']
    _format_rules = {'status': 'int'}


class RequestUpdateStat(RequestBase):
    _allow_keys = ['org_topic_id', 'topic_from', 'reply_count', 'popular_count']
    _format_rules = {'reply_count': 'int', 'popular_count': 'int'}


class RequestAddPictureDetect(RequestBase):
    _allow_keys = ['id', 'age', 'beauty', 'expression', 'face_shape', 'gender',
                   'glasses', 'quality', 'other']


if __name__ == '__main__':
    df = RequestAddTopic()
    df.org_topic_id = 12
    df.topic_from = "kami"
    print df.kami
    print df.org_topic_id
