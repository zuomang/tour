#!/usr/bin/env python
# -*- coding: utf-8 -*-

from access_token import get_access_token
import requests, json, parameter, urllib

info = urllib.quote_plus('http://www.quxhuan.com/info')
url_info = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s\
&redirect_uri=%s&response_type=code&scope=SCOPE&state=STATE' %(parameter.appid, info)
menu = {
    "button": [
        {
            "name": "我",
            "sub_button": [
                {
                    "type": "view",
                    "name": "我的资料",
                    "url": "http://82.254.158.115/info"
                }
            ]
        }
    ]
}

token = get_access_token()

url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" %token

# r = requests.post(url, data = json.dumps(menu, ensure_ascii=False))
# print r.text
print url_info