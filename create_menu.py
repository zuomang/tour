#!/usr/bin/env python
# -*- coding: utf-8 -*-

from access_token import get_access_token
import requests, json, parameter, urllib

info = urllib.quote_plus('http://www.quxhuan.com/info')
url_info = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE' %(parameter.appid, info)

menu = {
    "button": [
        {
            "name": "menu",
            "sub_button": [
                {
                    "type": "view",
                    "name": "1",
                    "url": url_info
                }
            ]
        }
    ]
}

token = get_access_token()

url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" %token

r = requests.post(url, data = json.dumps(menu, ensure_ascii=False))
if r.json().get('errcode') == 0:
	print "create menu success"
else:
	print r.json().get('errmsg')
# print url_info
