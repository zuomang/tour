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
    openid = session.get['openid']
    try:
        flag = Custormer.query.filter_by(openid = openid).first()
        return flag
    except Exception, e:
        print 'Exception: ', e
        db.session.rollback()

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
