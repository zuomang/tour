from flask import Flask, request, make_response
import time, hashlib
import parameter
import requests
import util

app = Flask(__name__)
app.config.from_envvar('FLASK_TEST_SETTINGS')

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
        return 'ok'

if __name__ == '__main__':
	app.run()
