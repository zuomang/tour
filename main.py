#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, request, make_response, render_template, g, session, redirect, url_for, jsonify, flash
from flask.ext.sqlalchemy import SQLAlchemy
from models.table import Custormer, Qun, member, db, Activity, ActivityDetail
from create_menu import url_qun
from payment import UnfiedOrder

import hashlib
import util

app = Flask(__name__)
app.config.from_envvar('FLASK_PRODUCT_SETTINGS')

def get_db():
	if not hasattr(g, 'db_session'):
		g.db_session = db.session
	return g.db_session

@app.before_request
def bind(*args, **kwargs):
	if request.method == 'GET' and request.path != '/activity' and request.path != '/' and not util.check_bing(request):
		return render_template('bing.html')

@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
	if request.method == 'GET':
		token = "cCPnbiQ3yFDEdkeQcEdf7jsX"
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
		else:
			return make_response()
	if request.method == 'POST':
		token = "cCPnbiQ3yFDEdkeQcEdf7jsX"
		query = request.args
		signature = query.get('signature', '')
		timestamp = query.get('timestamp', '')
		nonce = query.get('nonce', '')
		echostr = query.get('echostr', '')

		s = [timestamp, nonce, token]
		s.sort()
		s = ''.join(s)
		if (hashlib.sha1(s).hexdigest() == signature):
			return make_response(True)
		else:
			return make_response(False)

@app.route('/info', methods=['GET'])
def info():
	if request.method == 'GET':
		openid = session['openid']
		user = Custormer.query.filter_by(openid = openid).first()
		members = user.quns
		return render_template('info.html', user = user, members = members)

@app.route('/bing', methods=['POST'])
def bing():
	if request.method == 'POST':
		openid = session['openid']
		username = request.form['username']
		phone = request.form['phone']
		db = get_db()
		try:
			user = Custormer(openid, username, phone)
			db.add(user)
			db.commit()
		except Exception, ex:
			print 'Exception: ', ex
			db.rollback()
			return render_template('bing.html')
		else:
			members = user.quns
			return render_template('info.html', user = user, members = members)

@app.route('/qun', methods=['GET'])
def qun():
	if request.method == 'GET':
		openid = session['openid']
		try:
			user = Custormer.query.filter_by(openid = openid).first()
			my_qun = Qun.query.filter_by(openid = user.openid).first()
			quns = Qun.query.all()
		except Exception, e:
			print 'Exception: ', e
		else:
			my_quns = user.quns
			return render_template('qun.html', user = user, my_qun = my_qun, my_quns = my_quns, quns = quns)

@app.route('/qun/create', methods=['POST'])
def create():
	if request.method == 'POST':
		openid = session['openid']
		name = request.form['name']
		db = get_db()
		try:
			user = Custormer.query.filter_by(openid = openid).first()
			new_qun = Qun(name, user.phone, openid)
			user.quns.append(new_qun)
			db.add(new_qun)
			db.commit()
		except Exception, ex:
			print 'Exception: ', ex
			db.rollback()
			session.pop('_flashes', None)
			flash(u'创建群失败')
		finally:
			return redirect(url_for('qun'))

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
				return jsonify(err_code = 'E0001', err_msg = '加入失败，你已经加入过这个群')
			elif (len(user.quns) == 8):
				return jsonify(err_code = 'E0002', err_msg = '你最多只能加入八个群')
			else:
				qun.member_count += 1
				user.quns.append(qun)
				db.commit()
				return jsonify(err_code = 'E0000', err_msg = '你已成功加入')
		except Exception, e:
			print 'Exception: ', e
			db.rollback()

@app.route('/qun/exit', methods = ['POST'])
def qun_exit():
	if request.method == 'POST':
		openid = session['openid']
		qun_id = request.json['id']
		db = get_db()
		try:
			user = Custormer.query.filter_by(openid = openid).first()
			qun = Qun.query.filter_by(id = qun_id).first()
			if (qun not in user.quns):
				return jsonify(err_code = 'E0001', err_msg = '对不起，你还没有加入该群')
			else:
				user.quns.remove(qun)
				qun.member_count -= 1
				db.commit()
				return jsonify(err_code = 'E0000', err_msg = '你已经退出了该群')
		except Exception, e:
			print 'Exception: ', e
			db.rollback()

@app.route('/activity', methods = ['GET', 'POST'])
def activity():
	if request.method == 'GET':
			page_size = 10
			page_number = 1
			activity_count = len(Activity.query.all())
			activitys = Activity.query.paginate(page_number, page_size, False)
			return render_template('activity.html', activitys = activitys.items, count = activity_count)

	if request.method == 'POST':
		page_size = 10
		page_number = request.json['pageNumber']
		try:
			activity_count = len(Activity.query.all())
			activitys = Activity.query.paginate(page_number, page_size, False)
			if activitys:
				temp = util.list_and_obj(activitys.items)
				return jsonify({'err_code' : 'E0000', 'err_msg': 'success', 'data': temp, 'count': activity_count})
		except Exception, e:
			print 'Exception', e

@app.route('/activity/check', methods = ['GET', 'POST'])
def activity_check():
	if request.method == 'POST':
		openid = session['openid']
		activity_id = request.json['activityId']
		print activity_id
		# openid = session.get("openid")
		try:
			user = Custormer.query.filter_by(openid = openid).first()
			qun = Qun.query.filter_by(openid = openid).first()
		except Exception, e:
			print 'Exception', e
		else:
			if qun:
				return jsonify(err_code = 'E0000', err_msg = 'success')
			else:
				return jsonify(err_code = 'E0001', err_msg = '你还没有属于自己的群')


@app.route('/activity/join', methods = ['POST'])
def activity_join():
	if request.method == 'POST':
		openid = session['openid']
		activity_id = request.json['activityId']
		activity_date = request.json['date']
		activity_number= request.json['number']
		db = get_db()
		try:
			user = Custormer.query.filter_by(openid = openid).first()
			activity = Activity.query.filter_by(id = activity_id).first()
			detail = ActivityDetail(activity_id, activity.name, activity_date, openid, activity.id, activity_number, 100, 20)
			db.add(detail)
			db.commit()
		except Exception, e:
			print 'Exception', e
			db.rollback()
		else:
			if detail.id:
				return jsonify(err_code = 'E0000', err_msg = 'success')
			else:
				return jsonify(err_code = 'E0001', err_msg = '加入活动失败')


@app.route('/recharge', methods = ['GET', 'POST'])
def recharge():
	if request.method == 'GET':
		return render_template('recharge.html')

	if request.method == 'POST':
		print "request start........"
		openid = session['openid']
		amount = request.json['amount']
		print amount
		payment = UnfiedOrder()
        payment.setParameter("body", "test")
        payment.setParameter("total_fee", str(amout))
		payment.createXml()
		print payment.getPrepayId()
		return jsonify(err_code = 'EOOOO', err_msg = "success")


if __name__ == '__main__':
	app.run()
