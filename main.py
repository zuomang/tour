from flask import Flask, request, make_response, render_template, g
from flask.ext.sqlalchemy import SQLAlchemy
from models.custormer import Custormer
import time, hashlib
import parameter
import requests
import util

app = Flask(__name__)
app.config.from_envvar('FLASK_TEST_SETTINGS')
app.secret_key = 'test'
db = SQLAlchemy(app)

def get_db():
    if not hasattr(g, 'db_session'):
        g.db_session = db.session
    return g.db_session

@app.before_request
def before_request(*args, **kwargs):
	print '---------before_request----------'

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
			return render_template('info.html')

@app.route('/bing', methods=['POST'])
def bing():
    openid = session['openid']
    username = request.form('username')
    phone = request.form('phone')
    print openid, username, phone
    db = get_db()
    user = Custormer(openid, username, phone)
    db.add(user)
    temp = db.commit()
    if temp:
        return 'hello, world'
    else:
        return render_template('bing.html')

if __name__ == '__main__':
	app.run()
