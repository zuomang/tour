from flask import Flask, request, make_response
import time, hashlib

app = Flask(__name__)

app.config.update(
        SERVER_NAME='localhost',
        DEBUG=True
        )
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
        return 'hello, world'

if __name__ == '__main__':
	app.run(port=80)
