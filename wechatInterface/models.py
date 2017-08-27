from urllib import parse, request
from json import loads
from web.models import Subscription
import datetime
from math import ceil
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}


def get_access_token(wechat_id):
    wechat = Subscription.objects.get(id=wechat_id)
    get_parameter = {'appid': wechat.app_id, 'secret': wechat.app_secret}
    get_parameter = parse.urlencode(get_parameter)
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'
    response = request.Request(url='%s%s%s' % (url, '&', get_parameter), headers=header_dict)
    result = request.urlopen(response)
    result = loads(result.read().decode(encoding='utf-8'))
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
    get_parameter = {'access_token': access_token}
    get_parameter = parse.urlencode(get_parameter)
    url = '%s%s%s' % ('https://api.weixin.qq.com/cgi-bin/user/get', '?', get_parameter)
    response = request.Request(url=url, headers=header_dict)
    result = request.urlopen(response)
    fans = loads(result.read().decode(encoding='utf-8'))
    open_ids = []
    open_ids.append(fans['data']['openid'])
    if fans['total'] > fans['count']:
        i = ceil(fans['total'] / fans['count'])
        for fetch in range(0, i):
            get_parameter = {'next_openid': fans['next_openid']}
            get_parameter = parse.urlencode(get_parameter)
            url = '%s%s%s' % (url, '&', get_parameter)
            response = request.Request(url=url, headers=header_dict)
            result = request.urlopen(response)
            fans = loads(result.read().decode(encoding='utf-8'))
            open_ids.append(fans['data']['openid'])
    for open_id in open_ids:
        get_fans_data(open_id)
    return fans


def get_fans_data(open_id):
    return open_id
