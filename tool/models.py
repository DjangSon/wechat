from qiniu import Auth, put_data
from wechat.settings import Qiniu_App_Key, Qiniu_Secret_Key
import re


def base64_decode(base64):
    photo_list = ['jpeg', 'jpg', 'png', 'gif']
    pattern = re.compile(r'data:image/(\S+);base64,(\S+)')
    match = pattern.findall(base64.replace(' ', '+'))
    if match[0][0] not in photo_list:
        return False
    return match[0][1]


def upload(bucket, key, data):
    auth = Auth(Qiniu_App_Key, Qiniu_Secret_Key)
    token = auth.upload_token(bucket, key, 240)
    ret, info = put_data(token, key, data)
    return ret['key']
