#!/usr/bin/env python
# -*- coding: utf-8 -*-

from access_token import get_access_token
import requests, json, parameter, urllib

info = urllib.quote_plus('http://www.quxhuan.com/info')
qun = urllib.quote_plus('http://www.quxhuan.com/qun')
qun_manage = urllib.quote_plus('http://www.quxhuan.com/qun/manage')
new_activity = urllib.quote_plus('http://www.quxhuan.com/new_activity')
all_activity =  urllib.quote_plus('http://www.quxhuan.com/activity')
about = urllib.quote_plus('http://www.quxhuan.com/about')
token = get_access_token()

url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" %token
url_base = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE'
url_info = url_base %(parameter.appid, info)
url_qun = url_base %(parameter.appid, qun)
url_qun_manage = url_base %(parameter.appid, qun_manage)
url_new_activity = url_base %(parameter.appid, new_activity)
url_all_activity = url_base %(parameter.appid, all_activity)
url_about = url_base %(parameter.appid, about)

menu = {
	"button": [
        {
            "name": "关于撒欢",
            "sub_button": [
                {
                    "type": "view",
                    "name": "关于我们",
                    "url": url_about
                }
            ]
        },
			{
			"name": "活动",
			"sub_button": [
				{
					"type": "view",
					"name": "最新活动",
					"url": url_new_activity
				},
                {
                   "type": "view",
                    "name": "往期活动",
                    "url": url_all_activity
                }
			]
		},
		{
			"name": "我的撒欢",
			"sub_button": [
				{
					"type": "view",
					"name": "我的信息",
					"url": url_info
				},
				{
					"type": "view",
					"name": "我的群",
					"url": url_qun
				},
				{
					"type": "view",
					"name": "群管理",
					"url": url_qun_manage
				}
			]
		},
	]
}

if __name__ == '__main__':
	r = requests.post(url, data = json.dumps(menu, ensure_ascii=False))
	if r.json().get('errcode') == 0:
		print "create menu success"
	else:
	   print r.json().get('errmsg')
