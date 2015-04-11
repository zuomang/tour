#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import requests
from flask import session, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from models.user import User
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
	id = result.json().get('openid', '')
	session['openid'] = id
	return User.query.filter_by(openid=id).first()
