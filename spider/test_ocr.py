# -*- coding: utf-8 -*-
import base64
import json
from lib.util import *
from sdk.aip import AipFace

""" 你的 APPID AK SK """
APP_ID = '10121651'
API_KEY = 'pWF9SzypaaqEiAGNCu9FFkfL'
SECRET_KEY = 'OIOvTm1KS0GZKWOE5VWdGiAnzElrB6Zh'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

image = file_get_contents('./data/102.jpeg')
image = base64.b64encode(image)

imageType = "BASE64"

""" 调用人脸检测 """
#print client.detect(image, imageType)

""" 如果有可选参数 """

tmp_options = dict()
tmp_options["face_field"] = "age,beauty,expression,faceshape,gender,glasses,landmark," \
                            "race,quality,facetype"
tmp_options["max_face_num"] = 2
tmp_options["face_type"] = "LIVE"

""" 带参数调用人脸检测 """
res = client.detect(image, imageType, tmp_options)
print res['error_code'] == 0
print res['error_msg']
print type(res['error_code'])
print res['result']
print json.dumps(res['result'])