# -*- coding: utf-8 -*-


class ResponseBase(object):

    _allow_keys = ['result']

    def __setattr__(self, key, value):
        if key not in self._allow_keys:
            return False
        self.__dict__[key] = value


class ResponseAddTopic(ResponseBase):
    pass


class ResponseGetTopicList(ResponseBase):
    pass


class ResponseGetTopic(ResponseBase):
    pass


class ResponseAddPictures(ResponseBase):
    pass


class ResponseAddPictureContent(ResponseBase):
    pass


class ResponseGetPictureList(ResponseBase):
    pass


class ResponseGetPictureTotal(ResponseBase):
    pass


class ResponseUpdateStat(ResponseBase):
    pass


class ResponseAddPictureDetect(ResponseBase):
    pass


if __name__ == '__main__':
    df = ResponseGetPictureTotal()
    df.result = 12
    print type(df.result)
