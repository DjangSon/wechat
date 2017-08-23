from qiniu import Auth, put_data
from wechat.settings import Qiniu_App_Key, Qiniu_Secret_Key


def upload(bucket, key, data):
    auth = Auth(Qiniu_App_Key, Qiniu_Secret_Key)
    token = auth.upload_token(bucket, key, 240)
    ret, info = put_data(token, key, data)
    return ret['key']
