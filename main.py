#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, request, make_response, Response, render_template, g, session, redirect, url_for, jsonify, flash
from models.table import Custormer, Qun, db, Activity, ActivityDetail, PaymentOrder
from payment import UnfiedOrder, WechatConfigJsAPI, WechatJsPayment

import hashlib
import util

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
	if request.method == 'GET' and request.path != '/activity' and request.path != '/' and not util.check_bing(request):
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
		openid = session['openid']
		user = Custormer.query.filter_by(openid = openid).first()
		members = user.quns
		return render_template('info.html', user = user, members = members)


@app.route('/bing', methods=['POST'])
def bing():
	if request.method == 'POST':
		"""微信用户绑定"""
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
		"""群消息展示"""
		openid = session['openid']
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
		"""check是否是群主"""
		openid = session['openid']
		activity_id = request.json['activityId']
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
			qun = Qun.query.filter_by(openid = openid).first()
			amount = int(activity_number) * activity.partici_fee
			qun_building = qun.building_fund
			if amount>qun_building:
				detail = ActivityDetail(activity_id, activity.name, activity_date, openid, activity.id, activity_number, amount, 0)
				db.add(detail)
				db.commit()
				return jsonify(err_code = 'E0000', err_msg = '超过十人参加，有建设资金返还')
			else:
				qun.building_fund -= amount
			detail = ActivityDetail(activity_id, activity.name, activity_date, openid, activity.id, activity_number, amount, 0)
			db.add(detail)
			db.commit()
		except Exception, e:
			print 'Exception', e
			db.rollback()
		else:
			if detail.id:
				return jsonify(err_code = 'E0000', err_msg = '你已加入活动，记得准时参加')
			else:
				return jsonify(err_code = 'E0001', err_msg = '加入活动失败')


@app.route('/payment/getPaymentConf', methods = ['GET', 'POST'])
#@app.route('/paymenttest/getPaymentConf', methods = ['GET', 'POST'])
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
#@app.route('/paymenttest/recharge', methods = ['GET', 'POST'])
def recharge():

	if request.method == 'GET':
		"""GET方法返回充值页面"""
		return render_template('recharge.html')

	if request.method == 'POST':
		"""POST方法调用统一下单接口下单"""
		openid = session['openid']
		amount = int(request.json['amount'].encode('utf8'))*100 #充值金额单位为分
		payment = UnfiedOrder()
		payment.setParameter("body", "test")
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
					'return_msg': ''
				}
		else:
			response = {
					'return_code': 'FAIL',
					'return_msg': ''
				}
		xmlResponse = util.arrayToXml(response)
		return Response(xmlResponse, mimetype='text/xml;charset=UTF-8')


if __name__ == '__main__':
	app.run()
