import requests
import json
import os
import sys
from flask import Flask, Response
from flask import request
from flask import jsonify
#from flask import session

#from flask_restful import Resource, Api
app = Flask(__name__)
#api = Api(app)


#The key value store
kvs = {}
ip = os.environ['IP']
port = os.environ['PORT']
members = os.environ['MEMBERS']

#Initialize the first list of nodes =! primary node
membersk=str(members)
memberslist=membersk.split(',')
#This is the default master/primary node
masternode='5'

memberslistIds =[x[8:9] for x in memberslist]



@app.route('/myip')
def whatip():
	x = request.remote_addr
	return x + '\n'
	#return jsonify({'ip': request.remote_addr}), 200su

@app.route('/myport')
def whatport():
	x = request.host
	return x + '\n'

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
	if ipnum == 'localhost':
		return 0
	else:
		return 1
	#ipnode = ipnum[4:5]
	#return ipnode

def nodek():
	node = whatport()
	ipstr = str(node)
	ipsplit = ipstr.split(':')
	ipnum = ipsplit[1]
	ipnode = ipnum[4:5]
	return ipnode	

def isnode():
	node = whatport()
	ipstr = str(node)
	ipsplit = ipstr.split(':')
	ipnum = ipsplit[0]
	if ipnum[7:8] == '2':
		return True 
	else:
		return False

	#if (node=="10.0.0.1:49160"):
	#	return 'found'

@app.route('/testx')
def testx():
	x=whatport()
	return x
	#requests.get('http://localhost:49161/myport')

@app.route('/kvs/<key>', methods = ['PUT', 'GET', 'DELETE'])
def initKVS(key):

	# x = VALUE
	x = request.form.get('val')


	checknode = node()
	whichnode=nodek()

	#check if the request came from 
	#a node and not a user
	if checknode ==1:
		#check if this node is the master mode	
		if whichnode==masternode:
			#Do PUT
			if request.method == 'PUT':
				theResponse = kvsput(key, x)
				return theResponse

			#Do DELETE
			if request.method == 'DELETE':
				theResponse = kvsdel(key, x)
				return theResponse

			#Do GET		
			else:
				theResponse = kvsget(key, x)
				return theResponse
		else:
			if request.method == 'PUT':
				theResponse = kvsput(key, x)
				return theResponse

			#Do DELETE
			if request.method == 'DELETE':
				theResponse = kvsdel(key, x)
				return theResponse

			#Do GET		
			else:
				theResponse = kvsget(key, x)
				return theResponse
	else:
		if request.method == 'PUT':
				mainput = kvsput(key, x)
				theResponse = nodekvsput(key, x)
				if theResponse != 'Success':
					return mainput
				else:
					return theResponse

			#Do DELETE
		if request.method == 'DELETE':
			theResponse = kvsdel(key, x)
			return theResponse

		#Do GET		
		else:
			theResponse = kvsget(key, x)
			return theResponse
	


	
def nodekvsput(key, x):
	f = str(key)
	r = requests.put('http://10.0.0.20:12345/kvs/'+f , data = {'val':x})
	if r.status_code !=(200 or 201):
		return r.status_code
	else:
		return 'Success'

#def broadcastput(key,x):
#	for x in memberslistIds:



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
			#r = requests.get('http://10.0.0.22:12347/testx')
			data = {
			'replaced' : 0,
			'msg' : 'success'
			}
			#payload = {'val': x}
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
	app.run(host=ip, port=int(port))



