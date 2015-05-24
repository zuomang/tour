#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
from flask import session
from models.table import Custormer, db, Activity
from time import time

import json
import parameter
import requests
import xml.etree.ElementTree as ET

class JSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, Activity):
			return str(o)
		return json.JSONEncoder.default(self, o)

def now():
	return datetime.now()

def get_timestamp():
	timestamp = time()
	return int(timestamp)

def check_bing(request):
	openid = session.get('openid', None)
	if not openid:
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
	try:
		flag = Custormer.query.filter_by(openid = openid).first()
	except Exception, e:
		print 'Exception: ', e
		db.session.rollback()
	else:
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

def arrayToXml(arr):
	"""array转xml"""
	xml = ["<xml>"]
	for k, v in arr.iteritems():
		if v.isdigit():
			xml.append("<{0}>{1}</{0}>".format(k, v))
		else:
			xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
	xml.append("</xml>")
	return "".join(xml)

def xmlToArray(xml):
	"""将xml转为array"""
	array_data = {}
	root = ET.fromstring(xml)
	for child in root:
		value = child.text
		array_data[child.tag] = value
	return array_data