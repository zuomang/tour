from flask import Flask, request, make_response
import time, hashlib
import parameter
import requests
from models.token import Token

app = Flask(__name__)
app.config.from_envvar('FLASK_TEST_SETTINGS')

# @app.before_request
# def before_request(*args, **keys):
    # if request.method == 'GET':
        # code = request.args.get('code', '')
        # data = {
            # 'appid': parameter.appid,
            # 'secret': parameter.appsecret,
            # 'code': code,
            # 'grant_type': 'authorization_code'
        # }
        # result = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token', params = data)
        # id = result.json().get('openid', '')
        # r = Token.query.filter_by(openid = id).first()
        # if r:
            # print 'user had login'
            # return 'success'
        # else:
            # print 'user not login'
            # return 'error'

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
        print request.url
        print app.config['DEBUG']
        return 'hello, world'

if __name__ == '__main__':
	app.run()
