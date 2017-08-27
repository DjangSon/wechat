from urllib import parse, request
from json import loads
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}


def get_access_token(app_id, app_secret):
    get_parameter = {'appid': app_id, 'secret': app_secret}
    get_parameter = parse.urlencode(get_parameter)
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'
    response = request.Request(url='%s%s%s' % (url, '&', get_parameter), headers=header_dict)
    result = request.urlopen(response)
    result = loads(result.read().decode(encoding='utf-8'))
    return result


def get_all_fans(access_token):
    get_parameter = {'access_token': access_token}
    get_parameter = parse.urlencode(get_parameter)
    url = '%s%s%s' % ('https://api.weixin.qq.com/cgi-bin/user/get', '?', get_parameter)
    response = request.Request(url=url, headers=header_dict)
    result = request.urlopen(response)
    result = loads(result.read().decode(encoding='utf-8'))
    return result
