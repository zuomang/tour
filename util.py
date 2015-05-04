#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import requests
from flask import session, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from models.table import Custormer, db
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
	id = result.json().get('openid')
	session['openid'] = id
	try:
		flag = Custormer.query.filter_by(openid = id).first()
		db.session.commit()
	except StatementError, e:
		print 'StatementError: ', e
		db.session.rollback()
	except Exception, e:
		print 'Exception: ', e
	return flag