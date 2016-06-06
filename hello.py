import requests
import json
#import jsonify
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
memberslistIds =[x[8:9] for x in memberslist]

#This is the default master/primary node
masternode=min(memberslistIds)
memberslistIds.remove(masternode)


@app.route('/myip')
def whatip():
	x = request.remote_addr
	return x + '\n'
	#return jsonify({'ip': request.remote_addr}), 200su

@app.route('/myport')
def whatport():
	x = request.host
	return x

@app.route('/masters')
def master():
 	return memberslist[1]

@app.route('/check')
def check():
	a = int(masternode)
	b = a + 5
	c = str(b)
	return c

#TEST PARSING JSON RESPONSES FROM A NODE
@app.route('/cget')
def checkmasterx():
	r = requests.get('http://10.0.0.21:12346/kvs/foo')
	data=r.json()
	#x = data['key']
	return str(data['value'])

#CHECK IF THE IP ADDRESS IS FROM A NODE OR USER
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

#TEST SENDING AND RECEIVING MASTER NODE DATA
@app.route('/cmon')
def checkmaster():
	r = requests.get('http://10.0.0.20:12345/kk')
	x = nodek()
	return str(r.text) + '\n' + masternode + '\n' + x + '\n'

#RETURN NODE ID
@app.route('/kk')
def nodek():
	node = whatport()
	ipstr = str(node)
	ipsplit = ipstr.split(':')
	ipnum = ipsplit[0]
	ipnode = ipnum[8:9]
	return ipnode	

#CHECK IF THE IP ADDRESS IS FROM A NODE / SAME AS node()
def isnode():
	node = whatport()
	ipstr = str(node)
	ipsplit = ipstr.split(':')
	ipnum = ipsplit[0]
	if ipnum[7:8] == '2':
		return True 
	else:
		return False

def isMasterUser():
	node = whatport()
	ipstr = str(node)
	ipsplit = ipstr.split(':')
	ipnum = ipsplit[1]
	if ipnum[4:5] == '0':
		return True 
	else:
		return False

	#if (node=="10.0.0.1:49160"):
	#	return 'found'

#TEST RETURNING IP ADDRESS:PORT
@app.route('/testx')
def testx():
	x=whatport()
	return x
	#requests.get('http://localhost:49161/myport')

@app.route('/mast')
def testmaster():
	x = isMasterUser()
	return str(x)



#MAIN KVS PROGRAM
@app.route('/kvs/<key>', methods = ['PUT', 'GET', 'DELETE'])
def initKVS(key):

	# x = VALUE
	x = request.form.get('val')


	checknode = node()
	whichnode = nodek()
	p=isMasterUser()

	#check if the request came from 
	#a node and not a user
	if checknode ==1:
		#check if this node is the master mode	
		if whichnode==masternode:

			#Do PUT
			if request.method == 'PUT':
				mainput = kvsput(key, x)
				#theResponse = nodeputb(key, x)
				if mainput:
					return mainput
				else:
					return "leggo"

			#Do DELETE
			if request.method == 'DELETE':
				theResponse = kvsdel(key, x)
				return theResponse

			#Do GET		
			else:
				theResponse = kvsget(key)
				return theResponse
		else:
			#DO PUT
			if request.method == 'PUT':
				theResponse = kvsput(key, x)
				return "main"

			#Do DELETE
			if request.method == 'DELETE':
				theResponse = kvsdel(key, x)
				return theResponse

			#Do GET		
			else:
				theResponse = kvsget(key)
				return theResponse
	else:
		#DO PUT
		if request.method == 'PUT':
				mainput = kvsput(key, x)
				if p:
					return mainput
				else:
					theResponse = nodekvsput(key, x)
					#t = int(theResponse.status_code)
					if theResponse==("hmm"):
						return "alive"
					else:
						return str(theResponse)

		#Do DELETE
		if request.method == 'DELETE':
			theResponse = kvsdel(key, x)
			return theResponse
		#Do GET		
		else:
			theResponse = kvsget(key)
			if p:
				return theResponse
			else:
				secondresponse = nodekvsfuck(key)
				f = str(secondresponse)
				if f == 'Fail':
					return secondresponse
				else:
					return secondresponse


def nodekvsfuck(key):
	f = str(key)
	a = int(masternode)
	b = a +5
	c = str(b)
	r = requests.get('http://10.0.0.2'+ masternode + ':1234' + c + '/kvs/' + f)
	data=r.json()
	x = str(data['value'])
	d = kvsput(key, x)
	f = kvsget(key)
	p = str(r)
	if kvs.get(key)!= x:
		return f
	else:
		return f



#sends put to master
def nodekvsput(key, x):
	f = str(key)

	a = int(masternode)
	b = a + 5
	c = str(b)

	r = requests.put('http://10.0.0.2'+ masternode + ':1234' + c + '/kvs/' + f, data = {'val':x})
	#r = requests.put('http://10.0.0.21:12346/kvs/' + f, data = {'val':x})
	#response=r.json()
	#t = int(r.status_code)
	x = str(r.text)
	if x ==("leggo"):
		return "hmm"
	else:
		return str(r)



def nodeputb(key, x):
	f = str(key)

 	for z in memberslistIds:
 		a = int(z)
		b = a +5
		c = str(b)
 		req = requests.put('http://10.0.0.2' + z + ':1234' + c + '/kvs/'+f , data = {'val':x})
 	return "fire"
 	#return 'Fail'

 		#if req.status_code!=(200 or 201):
 		#	return req.status_code
 		#else:
 		#	return 'Success'


def kvsget(key):
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
			'msg' : 'success',
			'membersIDS': memberslistIds,
			'masterID':masternode
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

@app.route('/mem')
def mem():
	for z in memberslistIds:
 		a = int(z)
		b = a +5
		c = str(b)
		return c


#def checkT(key, value):

#def checkmaster(key):
#	cmaster=requests.get(https://localhost:49160)


if __name__ == '__main__':
	#x = 'asd'
	#f = hash(x, 10)
	#print f
	app.debug = True
	app.run(host=ip, port=int(port))



