#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import requests
from flask import session, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from models.table import Custormer, db, Activity
import parameter
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Activity):
            return str(o)
        return json.JSONEncoder.default(self, o)

def now():
	return datetime.now()

def check_bing(request):
    if session.get('openid'):
        return Custormer.query.filter_by(openid = id).first()
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
        try:
		    flag = Custormer.query.filter_by(openid = id).first()
		    db.session.commit()
        except Exception, e:
		    print 'Exception: ', e
		    db.session.rollback()
        return flag

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
