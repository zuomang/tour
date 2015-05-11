#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
from flask import session
from models.table import Custormer, db, Activity
import json
import parameter
import requests

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Activity):
            return str(o)
        return json.JSONEncoder.default(self, o)

def now():
	return datetime.now()

def check_bing(request):
    openid = session.get('openid', None)
    if openid:
        flag = Custormer.query.filter_by(openid = openid).first()
        print "-----------session:flag---------: ", flag
        if flag:
            return True
        else:
            return False
    else:
        code = request.args.get('code', '')
        data = {
                'appid': parameter.appid,
                'secret': parameter.appsecret,
                'code': code,
                'grant_type': 'authorization_code'
                }
        result = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token', params = data)
        id = result.json().get('openid')
        session['openid'] = id
        flag = Custormer.query.filter_by(openid = id).first()
        print "------------wechat:flag---------: ", flag
        if flag:
            return True
        else:
            return False

def obj_to_dict(obj):
	pr = {}
	pr['id'] = obj.id
	pr['name'] = obj.name
	pr['partici_fee'] = obj.partici_fee
	pr['owner'] = obj.owner
	pr['cost'] = obj.cost
	pr['description'] = obj.description
	return pr

def list_and_obj(activitys):
	temp = []
	for a in activitys:
		t = obj_to_dict(a)
		temp.append(t)
	return temp
