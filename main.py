#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, request, make_response, Response, render_template, g, session, redirect, url_for, jsonify, flash
from models.table import Custormer, Qun, db, Activity, ActivityDetail, PaymentOrder
from payment import UnfiedOrder, WechatConfigJsAPI, WechatJsPayment

import hashlib
import util
import re

app = Flask(__name__)
app.config.from_envvar('FLASK_PRODUCT_SETTINGS')

def get_db():
	"""配置全局数据源"""
	if not hasattr(g, 'db_session'):
		g.db_session = db.session
	return g.db_session

@app.before_request
def bind(*args, **kwargs):
	"""拦截器：验证用户是否绑定"""
	if request.method == 'GET' and request.path != '/' and not util.check_bing(request):
		pattern = re.compile(r'^/activity.*')
		match = pattern.match(request.path)
		if not match:
			return render_template('bing.html')

@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
	if request.method == 'GET':
		"""微信后台接口配置验证"""
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
		"""微信推送过来消息验证"""
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
			return make_response("True")
		else:
			return make_response("False")


@app.route('/info', methods=['GET'])
def info():
	if request.method == 'GET':
		"""个人信息页面"""
		openid = session.get('openid')
		user = Custormer.query.filter_by(openid = openid).first()
		members = user.quns
		return render_template('info.html', user = user, members = members)


@app.route('/bing', methods=['GET', 'POST'])
def bing():
	if request.method == 'GET':
		return render_template('bing.html')
	if request.method == 'POST':
		"""微信用户绑定"""
		openid = session.get('openid')
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
		"""群消息展示"""
		openid = session.get('openid')
		try:
			user = Custormer.query.filter_by(openid = openid).first()
			my_qun = Qun.query.filter_by(openid = openid).first()
			quns = Qun.query.all()
		except Exception, e:
			print 'Exception: ', e
		else:
			my_quns = user.quns
			return render_template('qun.html', user = user, my_qun = my_qun, my_quns = my_quns, quns = quns)


@app.route('/qun/create', methods=['POST'])
def create():
	if request.method == 'POST':
		"""创建群"""
		openid = session.get('openid')
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
		openid = session.get('openid')
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
		openid = session.get('openid')
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

@app.route('/qun/manage', methods = ['GET', 'POST'])
def qun_manage():
	if request.method == 'GET':
		openid = session.get('openid')
		#openid = 'okPmMs8zQGo2440Z5WzRImozRjI4'
		try:
			qun = Qun.query.filter_by(openid = openid).first()
			members = qun.custormers
		except Exception, e:
			print 'Exception: ', e
		else:
			return render_template("members.html", members = members)

	if request.method == 'POST':
		openid = session.get('openid')
		#openid = 'okPmMs8zQGo2440Z5WzRImozRjI4'
		phone = str(request.json['phone'])
		search_custormer = Custormer.query.filter_by(phone = phone).first()
		qun = Qun.query.filter_by(openid = openid).first()

		if not search_custormer:
			return jsonify(err_code = "E0001", err_msg = "此用户不存在")
		else:
			if search_custormer in qun.custormers:
				print "用户已加入"
				return jsonify(err_code = "E0000", err_msg = "delete", openid = search_custormer.openid, name = search_custormer.username)
			else:
				print "用户还没加入"
				return jsonify(err_code = "E0000", err_msg = "add", openid = search_custormer.openid, name = search_custormer.username)


@app.route('/qun/manage/delete', methods = ['POST'])
def qun_manage_delete():
	if request.method == 'POST':
		openid = session.get('openid')
		#openid = 'okPmMs8zQGo2440Z5WzRImozRjI4'
		delete_id = request.json['deleteId']
		db = get_db()

		custormer = Custormer.query.filter_by(openid = delete_id).first()
		qun = Qun.query.filter_by(openid = openid).first()
		if custormer in qun.custormers:
			try:
				qun.custormers.remove(custormer)
				qun.member_count -= 1
				db.commit()
			except Exception, e:
				print 'Exception: ', e
				db.rollback()
			else:
				return jsonify(err_code = "E0000", err_msg = "删除用户成功")
		else:
			return jsonify(err_code = "E0001", err_msg = "您的群没有该用户")

@app.route('/qun/manage/add', methods = ['POST'])
def qun_manage_add():
	if request.method == 'POST':
		openid = session.get('openid')
		#openid = 'okPmMs8zQGo2440Z5WzRImozRjI4'
		#test
		add_id = request.json['id']
		db = get_db()

		custormer = Custormer.query.filter_by(openid = add_id).first()
		qun = Qun.query.filter_by(openid = openid).first()
		if len(custormer.quns) >= 8:
			return jsonify(err_code="E0001", err_msg = "该用户已经加入了8个群")

		if custormer in qun.custormers:
			return jsonify(err_code = "E0001", err_msg = "您的群里已有该用户")
		else:
			try:
				qun.custormers.append(custormer)
				qun.member_count += 1
				db.commit()
			except Exception, e:
				print 'Exception: ', e
				db.rollback()
			else:
				return jsonify(err_code = "E0000", err_msg = "成功添加该用户")


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
		"""check是否是群主"""
		openid = session.get('openid')
		custormer = Custormer.query.filter_by(openid = openid).first()
		if custormer:
			try:
				qun = Qun.query.filter_by(openid = openid).first()
			except Exception, e:
				print 'Exception', e
			else:
				if qun:
					return jsonify(err_code = 'E0000', err_msg = 'success')
				else:
					return jsonify(err_code = 'E0001', err_msg = '你还没有属于自己的群')
		else:
			return jsonify(err_code = 'E0002', err_msg = '<a href="http://quxhuan.com/bing">点击绑定</a>')


@app.route('/activity/join', methods = ['POST'])
def activity_join():
	if request.method == 'POST':
		openid = session.get('openid')
		activity_id = request.json['activityId']
		activity_number= request.json['number']
		db = get_db()
		try:
			activity = Activity.query.filter_by(id = activity_id).first()
			qun = Qun.query.filter_by(openid = openid).first()
			amount = int(activity_number) * activity.partici_fee
			qun_building = qun.building_fund
			if amount>qun_building:
				return jsonify(err_code = 'E0002', err_msg = '群建设资金不足，前往充值')
			else:
				qun.building_fund -= amount
			detail = ActivityDetail(activity_id, activity.name, openid, activity.id, activity_number, amount, 0)
			db.add(detail)
			db.commit()
		except Exception, e:
			print 'Exception', e
			db.rollback()
		else:
			if detail.id and detail.accompany_count < 10:
				return jsonify(err_code = 'E0000', err_msg = '你已加入活动，参加人数超过十人可享受群建设资金返还')
			elif detail.id and detail.accompany_count >= 10:
				return jsonify(err_code = 'E0000', err_msg = '你已加入活动，活动完毕你将会收到群建设资金返还')
			else:
				return jsonify(err_code = 'E0001', err_msg = '加入活动失败')


@app.route('/activity/detail/<int:activity_id>', methods = ['GET'])
def activity_detail(activity_id):
	"""活动详情页面"""
	if request.method == 'GET':
		activity = Activity.query.filter_by(id = activity_id).first()
		return render_template('activity_detail.html', activity = activity)


@app.route('/activity/new', methods = ['GET'])
def new_activity():
	"""最新活动页面"""
	if request.method == 'GET':
		activitys = Activity.query.order_by(Activity.create_time).limit(5)
		return render_template('activity.html', activitys = activitys, count = 5)

@app.route('/payment/getPaymentConf', methods = ['GET', 'POST'])
def getPaymentConf():
	if request.method == 'GET':
		"""微信SDK config 验证"""
		jsPay = WechatConfigJsAPI()
		jsPay.createDate()
		result = jsPay.getResult()
		return jsonify(err_code = 'E0000', err_msg = 'success', data = result )

	if request.method == 'POST':
		"""H5页面JS API发起支付"""
		wechatPayment = WechatJsPayment()
		prepayid = request.form['prepayid']
		result = wechatPayment.getParameters(prepayid)
		return jsonify(err_code = 'E0000', err_msg = "success", data = result)


@app.route('/payment/recharge', methods = ['GET', 'POST'])
def recharge():

	if request.method == 'GET':
		"""GET方法返回充值页面"""
		return render_template('recharge.html')

	if request.method == 'POST':
		"""POST方法调用统一下单接口下单"""
		openid = session.get('openid')
		amount = int(request.json['amount'].encode('utf8'))*100 #充值金额单位为分
		payment = UnfiedOrder()
		payment.setParameter("body", "建设资金充值")
		payment.setParameter("total_fee", str(amount))
		payment.setParameter("openid", openid)
		payment.createXml()
		data = {
			"prepayid": payment.getPrepayId()
			}
		return jsonify(err_code = 'E0000', err_msg = "success", data = data )


@app.route('/payback', methods = ['POST', 'GET'])
def paymentCallback():
	"""payback负责微信支付回调"""
	if request.method == "POST":
		call_data = util.xmlToArray(request.data)
		if call_data.get('result_code') == "SUCCESS" and call_data.get('return_code') == "SUCCESS":
			db = get_db()
			try:
				order = PaymentOrder(call_data["bank_type"], call_data["cash_fee"], call_data["fee_type"], call_data["is_subscribe"], call_data["openid"], call_data["out_trade_no"],
					call_data["result_code"], call_data["time_end"], call_data["total_fee"], call_data["trade_type"], call_data["transaction_id"])
				db.add(order)
				owner_qun = Qun.query.filter_by(openid = call_data["openid"]).first()
				owner_qun.building_fund += float(call_data["total_fee"])/100
				db.commit()
			except Exception, e:
				print "Exception: ", e
				db.rollback()
			else:
				response = {
					'return_code': 'SUCCESS',
				}
		else:
			response = {
					'return_code': 'FAIL',
					'return_msg': ''
				}
		xmlResponse = util.arrayToXml(response)
		return Response(xmlResponse, mimetype='text/xml;charset=UTF-8')

@app.route('/about', methods = ['GET'])
def about():
	if request.method == 'GET':
		return render_template('about.html')

if __name__ == '__main__':
	app.run()
