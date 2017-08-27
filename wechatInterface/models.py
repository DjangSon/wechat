from urllib import parse, request
from json import loads
from web.models import Subscription
import datetime
from math import ceil
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}


def get_access_token(wechat_id):
    wechat = Subscription.objects.get(id=wechat_id)
    get_parameter = parse.urlencode({'appid': wechat.app_id, 'secret': wechat.app_secret})
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'
    result = http_request(url='%s%s%s' % (url, '&', get_parameter))
    if 'access_token' in result:
        wechat.access_token = result['access_token']
        wechat.last_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        wechat.save()
        return result['access_token']
    return False


def get_all_fans(wechat_id):
    last_date = datetime.datetime.now() + datetime.timedelta(hours=1.8)
    wechat = Subscription.objects.filter(id=wechat_id, last_date__lte=last_date)
    if wechat.exists():
        access_token = get_access_token(wechat_id)
    else:
        access_token = wechat.access_token
    open_ids = []
    get_parameter = parse.urlencode({'access_token': access_token})
    url = '%s%s%s' % ('https://api.weixin.qq.com/cgi-bin/user/get', '?', get_parameter)
    fans = http_request(url=url)
    open_ids.append(fans['data']['openid'])
    if fans['total'] > fans['count']:
        i = ceil(fans['total'] / fans['count'])
        for fetch in range(0, i):
            get_parameter = parse.urlencode({'next_openid': fans['next_openid']})
            fans = http_request(url='%s%s%s' % (url, '&', get_parameter))
            open_ids.append(fans['data']['openid'])
    for open_id in open_ids:
        get_fans_data(open_id=open_id, access_token=access_token)
    return fans


def get_fans_data(open_id, access_token):
    get_parameter = parse.urlencode({'access_token': access_token, 'openid': open_id, 'lang': 'zh_Cn'})
    url = '%s%s%s' % ('https://api.weixin.qq.com/cgi-bin/user/info?', '&', get_parameter)
    result = http_request(url=url)
    return result


def batch_get_fans_data(access_token):
    get_parameter = parse.urlencode({'access_token': access_token})
    url = '%s%s%s' % ('https://api.weixin.qq.com/cgi-bin/user/info/batchget', '?', get_parameter)
    result = http_request(url=url)
    return result


def http_request(url):
    response = request.Request(url=url, headers=header_dict)
    result = request.urlopen(response)
    result = loads(result.read().decode(encoding='utf-8'))
    return result
