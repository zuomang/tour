#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import requests
from flask import session
from flask.ext.sqlalchemy import SQLAlchemy
from models.User import User

def now():
    return datetime.now()

# @app.before_request
# def before_request(*args, **keys):
#     if request.method == 'GET':
#         code = request.args.get('code', '')
#         data = {
#             'appid': parameter.appid,
#             'secret': parameter.appsecret,
#             'code': code,
#             'grant_type': 'authorization_code'
#         }
#         result = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token', params = data)
#         id = result.json().get('openid', '')
#         r = Token.query.filter_by(openid = id).first()
#         if r:
#             print 'user had login'
#             return 'success'
#         else:
#             print 'user not login'
#             return 'error'
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

	if User.query.filter_by(openid=id).first() == None:
		return render_template('bing.html')