#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import requests
from flask import session, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from models.table import Custormer
import parameter

def now():
    return datetime.now()

def check_bing(request):
 	code = request.args.get('code', '')
	data = {
    	'appid': parameter.appid,
    	'secret': parameter.appsecret,
    	'code': code,
    	'grant_type': 'authorization_code'
	}
	result = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token', params = data)
	openid = result.json().get('openid')
	session['openid'] = openid
	custormer = Custormer.query.filter_by(openid = openid).first()
	if custormer:
		return True
	else:
		return False
