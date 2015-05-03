#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, request, make_response, render_template, g, session, redirect, url_for, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from models.table import Custormer, Qun, member, db
from create_menu import url_qun
import hashlib
import util
app = Flask(__name__)
app.config.from_envvar('FLASK_TEST_SETTINGS')
app.secret_key = 'test'

def get_db():
	if not hasattr(g, 'db_session'):
		g.db_session = db.session
	return g.db_session

@app.route('/', methods=['GET'])
def wechat_auth():
	if request.method == 'GET':
		token = "test"
		query = request.args
		signature = query.get('signature', '')
		timestamp = query.get('timestamp', '')
		nonce = query.get('nonce', '')
		echostr = query.get('echostr', '')

		s = [timestamp, nonce, token]
		s.sort()
		s = ''.join(s)
		if (hashlib.sha1(s).hexdigest() == signature):
			return make_response(echostr)

@app.route('/info', methods=['GET'])
def info():
	if request.method == 'GET':
		if util.check_bing(request) == None:
			return render_template('bing.html')
		else:
			openid = session['openid']
			user = Custormer.query.filter_by(openid = openid).first()
			members = user.quns
			return render_template('info.html', user = user, members = members)

@app.route('/bing', methods=['POST'])
def bing():
	openid = session['openid']
	username = request.form['username']
	phone = request.form['phone']
	db = get_db()
	user = Custormer(openid, username, phone)
	db.add(user)
	try:
		db.commit()
	except Exception, ex:
		print 'Exception: ', ex
		return render_template('bing.html')
	else:
		members = user.quns
		return render_template('info.html', user = user, members = members)

@app.route('/qun', methods=['GET'])
def qun():
	if request.method == 'GET':
		if util.check_bing(request) == None:
			return render_template('bing.html')
		else:
			openid = session['openid']
			user = Custormer.query.filter_by(openid = openid).first()
			my_qun = Qun.query.filter_by(openid = user.openid).first()
			my_quns = user.quns
			quns = Qun.query.all()
			return render_template('qun.html', user = user, my_qun = my_qun, my_quns = my_quns, quns = quns)

@app.route('/qun/create', methods=['POST'])
def create():
	openid = session['openid']
	db = get_db()
	user = Custormer.query.filter_by(openid = openid).first()

	name = request.form['name']
	build = request.form['build']
	new_qun = Qun(name, user.phone, openid, build)
	user.quns.append(new_qun)
	db.add(new_qun)
	try:
		db.commit()
	except Exception, ex:
		print 'Exception: ', ex
	finally:
		return redirect(url_qun)

@app.route('/qun/info', methods=['POST'])
def qun_info():
	if request.method == 'POST':
		qun_id = request.json['id']
		openid = session['openid']
		db = get_db()
		try:
			user = Custormer.query.filter_by(openid = openid).first()
			qun = Qun.query.filter_by(id = qun_id).first()
			if (qun in user.quns):
				pass
                #return jsonify(err_code = 'E0001', err_msg = '加入失败，你已经加入过这个群')
			elif (len(user.quns) == 8):
				return jsonify(err_code = 'E0002', err_msg = '你最多只能加入八个群')
			else:
				qun.member_count += 1
				user.quns.append(qun)
				db.commit()
				return jsonify(err_code = 'E0000', err_msg = '你已成功加入')
		except Exception, e:
			print 'Exception: ', e

if __name__ == '__main__':
	app.run()
