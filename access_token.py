#!/usr/bin/env python
# encoding: utf-8

import requests, parameter, json

def get_access_token():
    appid = parameter.appid
    secret = parameter.appsecret
    url = 'https://api.weixin.qq.com/cgi-bin/token?\
grant_type=client_credential&appid=%s&secret=%s' %(appid, secret)
    result = requests.get(url)
    print json.loads(result.text).get('access_token')
    return json.loads(result.text).get('access_token')

if __name__ == '__main__':
    get_access_token()
