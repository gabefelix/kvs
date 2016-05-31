import requests
import json
from flask import Flask, Response
from flask import request
from flask import jsonify
#from flask import session

#from flask_restful import Resource, Api
app = Flask(__name__)
#api = Api(app)


#The key value store
kvs = {}

#This is the default master/primary node
masternode=0


@app.route('/myip')
def whatip():
	x = request.remote_addr
	return x
	#return jsonify({'ip': request.remote_addr}), 200su

@app.route('/myport')
def whatport():
	x = request.host
	return x

@app.route('/hello')
def hello_world():
	#if request.method == 'POST':
	#	app.error_handler_spec[None][405] = METHOD_NOT_ALLOWED
	return 'Hello World!'


@app.route('/echo')
def echobot():
		msg = request.args.get('msg')
		if msg is None:
			return ""
		else:
			return msg


@app.route('/test')
def node():
	node = whatport()
	ipstr = str(node)
	ipsplit = ipstr.split(':')
	ipnum = ipsplit[0]
	ipnode = ipnum[8:9]
	return ipnode

	#if (node=="10.0.0.1:49160"):
	#	return 'found'

@app.route('/kvs/<key>', methods = ['PUT', 'GET', 'DELETE'])
def initKVS(key):

	# x = VALUE
	x = request.form.get('val')

	thisnode = node()
	if thisnode==masternode:
		#Do PUT
		if request.method == 'PUT':
			theResponse = kvsput(key, x)
			return theResponse

		#Do DELETE
		if request.method == 'DELETE':
			theResponse = kvsput(key, x)
			return theResponse

		#Do GET		
		else:
			theResponse = kvsput(key, x)
			return theResponse


def kvsget(key,x):
	if kvs.get(key) == None:
			data = {
			'msg' : 'error',
			'error' : 'key does not exist'
			}
			response = jsonify(data)
			response.status_code = 404
			return response
		#key value does exist
	else:
			x = kvs.get(key)
			data = {
			'msg' : 'success',
			'value' : x
			}
			response = jsonify(data)
			response.status_code = 404
			return response	

def kvsdel(key,x):
	if kvs.get(key) == None:
			data = {
			'msg' : 'error',
			'error' : 'key does not exist'
			}
			response = jsonify(data)
			response.status_code = 404
			return response
	else:
			del kvs[key]
			data = {
			'msg' : 'success'
			}
			response = jsonify(data)
			response.status_code = 200
			return response

#insert into kvs
def kvsput(key, x):
	if kvs.get(key) == None:
			kvs[key] = x
			r = requests.get('http://10.0.0.20:12345/kvs/foo')
			data = {
			'replaced' : 0,
			'msg' : 'success',
			'status': r.status_code
			}
			payload = {'val': x}
			response = jsonify(data)
			response.status_code = 201
			return response

		#replace value of key with new value	
	else:
			kvs[key] =x
			data = {
			'replaced' : 1,
			'msg' : 'success'
			}
			response = jsonify(data)
			response.status_code = 200
			return response	

#def checkT(key, value):

#def checkmaster(key):
#	cmaster=requests.get(https://localhost:49160)


if __name__ == '__main__':
	#x = 'asd'
	#f = hash(x, 10)
	#print f
	app.debug = True
	app.run(host='0.0.0.0',port=12345)
	app.run(host='0.0.0.0',port=12346)
	app.run(host='0.0.0.0',port=12347)
	app.run(host='0.0.0.0', port = 49160)
	app.run(host='0.0.0.0', port = 49161)
	app.run(host='0.0.0.0', port = 49162)


