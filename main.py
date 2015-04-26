from flask import Flask, request, make_response, render_template, g, session
from flask.ext.sqlalchemy import SQLAlchemy
from models.table import Custormer, Qun, member
import time, hashlib
import parameter
import requests
import util

app = Flask(__name__)
app.config.from_envvar('FLASK_TEST_SETTINGS')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zmyjy1314@localhost/test'
app.secret_key = 'test'
db = SQLAlchemy(app)

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
			user = Custormer.query.filter_by(openid = session['openid']).first()
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
			my_qun = Qun.query.filter_by(openid = openid).first()
			quns = user.quns
			return render_template('qun.html', user = user, qun = my_qun, quns = quns)

if __name__ == '__main__':
	app.run()
