#!/usr/bin/env python
# -*- coding: utf-8 -*-

from access_token import get_access_token
import requests, json, parameter, urllib

info = urllib.quote_plus('http://www.quxhuan.com/info')
qun = urllib.quote_plus('http://www.quxhuan.com/qun')
qun_manage = urllib.quote_plus('http://www.quxhuan.com/qun/manage')
my_activity = urllib.quote_plus('http://www.quxhuan.com/my_activity')
all_activity =  urllib.quote_plus('http://www.quxhuan.com/activity')
token = get_access_token()

url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" %token
url_base = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE'
url_info = url_base %(parameter.appid, info)
url_qun = url_base %(parameter.appid, qun)
url_qun_manage = url_base %(parameter.appid, qun_manage)
url_my_activity = url_base %(parameter.appid, my_activity)
url_all_activity = url_base %(parameter.appid, all_activity)

menu = {
	"button": [
			{
			"name": "活动",
			"sub_button": [
				{
					"type": "view",
					"name": "全部信息",
					"url": url_all_activity
				}
			]
		},
		{
			"name": "我",
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
		}
	]
}

if __name__ == '__main__':
	r = requests.post(url, data = json.dumps(menu, ensure_ascii=False))
	if r.json().get('errcode') == 0:
		print "create menu success"
	else:
	   print r.json().get('errmsg')
