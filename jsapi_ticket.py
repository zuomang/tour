#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
from models.table import Token, db
from access_token import get_access_token

import requests

def create_jsapi_ticket():
	token = get_access_token()
	url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi" %token
	result = requests.get(url)
	if result.json().get("errcode") == 0:
		return result.json().get("ticket")

def get_jsapi_ticket():
	now = datetime.now()
	try:
		current_ticket = Token.query.filter_by(name = 'jsapi_ticket').first()
		interval = now - current_ticket.time
		if interval.seconds < 7000:
			return current_ticket.token
		else:
			new_ticket = create_jsapi_ticket()
			new_time = datetime.now()
			current_ticket.token = new_ticket
			current_ticket.time = new_time
			db.session.commit()
			return new_ticket
	except Exception, e:
		print 'Exception', e
		db.session.rollback()

if __name__ == '__main__':
	jsapi_ticket = create_jsapi_ticket()
	print jsapi_ticket
	ticket = Token('jsapi_ticket', jsapi_ticket)
	db.session.add(ticket)
	db.session.commit()
