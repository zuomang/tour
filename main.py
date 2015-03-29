from flask import Flask, request, make_response
import time, hashlib

app = Flask(__name__)

@app.route('/weixin', methods=['GET'])
def wechat_auth():
	if request.method == 'GET':
		token = "genchlife"
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

if __name__ == '__main__':
	app.run(host='0.0.0.0')