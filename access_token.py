#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
from models.table import Token, db
import requests, parameter, json

def create_access_token():
	appid = parameter.appid
	secret = parameter.appsecret
	url = 'https://api.weixin.qq.com/cgi-bin/token?\
grant_type=client_credential&appid=%s&secret=%s' %(appid, secret)
	result = requests.get(url)
	return json.loads(result.text).get('access_token')

def get_access_token():
	now = datetime.now()
	try:
		current_token = Token.query.filter_by(name = 'access_token').first()
		interval = now - current_token.time
		if interval.seconds < 7000:
			print "return old token"
			return current_token.token
		else:
			print "return new token"
			new_token = create_access_token()
			new_time = datetime.now()
			current_token.token = new_token
			current_token.time = new_time
			db.session.commit()
			return new_token
	except Exception, e:
		print 'Exception', e
		db.session.rollback()

if __name__ == '__main__':
	access_token = create_access_token()
	token = Token('access_token', access_token)
	db.session.add(token)
	db.session.commit()
