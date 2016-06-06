import requests
import json
#import jsonify
#import grequests
#import gevent
import threading
import os
import sys
from flask import Flask, Response
from flask import request
from flask import jsonify
from flask import Flask, abort

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

memberslist[:] = ['http://' + x for x in memberslist]



@app.route('/myip')
def whatip():
	x = request.remote_addr
	return x + '\n'
	#return jsonify({'ip': request.remote_addr}), 200su

@app.route('/myport')
def whatport():
	x = request.host
	return x + '\n'

@app.route('/masters')
def master():
 	return memberslist[1]

@app.route('/check')
def check():
	a = int(masternode)
	b = a + 5
	c = str(b)
	return c

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

@app.route('/')

#NODE ID#
def nodek():
	node = whatport()
	ipstr = str(node)
	ipsplit = ipstr.split(':')
	ipnum = ipsplit[1]
	ipnode = ipnum[4:5]
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

	#if (node=="10.0.0.1:49160"):
	#	return 'found'

#RETURN IP ADDRESS:PORT
@app.route('/testx')
def testx():
	x=whatport()
	return x
	#requests.get('http://localhost:49161/myport')

"""
def bcast(val):
	batch = '[{"method": "PUT", "path": "http://10.0.0.21:12346/kvs/boo", "body": {"val":val}}, {"method": "PUT", "path": "http://10.0.0.21:12346/kvs/boo", "body": {"val":val}}]'
	try:
		requests = json.loads(batch)
	except ValueError as e:
		abort(400)

	responses = []

	for index, req in enumerate(requests):
		method = req['method']
		path = req['path']
		body = req.get('body', None)
		print method + '\n' + path + '\n' + body

		with app.app_context():
			with app.test_request_context(path, method=method, data=body):
				try:
					rv = app.preprocess_request()

					if rv is None:
						# Main Dispatch
						rv = app.dispatch_request()
				except Exception as e:
					rv = app.handle_user_exception(e)

					response = app.make_response(rv)

				# Post process Request
				response = app.process_response(response)

		# Response is a Flask response object.
		# _read_response(response) reads response.response 
		# and returns a string. If your endpoints return JSON object,
		# this string would be the response as a JSON string.
		responses.append({
			"status": response.status_code,
			"response": _read_response(response)
		})

	return make_response(json.dumps(responses), 207, HEADERS)
"""

def hookbak(request, val, *args, **kwargs):
	print request 
	if request:
		try:
			res = requests.put(request.pop(), data = {'val':val}, timeout = 5)
			return res.status_code
		except requests.exceptions.Timeout:
			print "hook timeout \n"
			return "hook failed"
	else:
		return "No mo\n"

def bcast(members, val):
	if not members:
		return "all done\n"
	member = members.pop()
	try: 
		print member + " requester space\n"
		resp = requests.put(member, data = {'val':val}, timeout = 5, hooks = {'response': bcast(members, val)})
		#'members':members
		return "titys!"
	except requests.exceptions.Timeout:
		#print members
		print "timedout\n"
		return "dick!"



#MAIN KVS PROGRAM
@app.route('/kvs/<key>', methods = ['PUT', 'GET', 'DELETE'])
def initKVS(key):
	#hooks = {request: bcast}

	#if empty request.info: return 
	# x = VALUE

	x = request.form.get('val')
	#y = request.get_json(force=True)
	#print y
	"""
	y = request.form.get('members')
	print y
	# members is empty and localhost is calling, let it through, otherwise stop the insanity
	if not y:
		locdog = node()
		if locdog != 0:
			return
	"""

	if request.method == 'PUT':

		#bcast(x)
		res = kvsput(key, x)
		urls = [i + '/kvs/' + key for i in memberslist]
		print memberslist
		print urls
		reals = [j.encode('ascii') for j in urls]
		print reals
		bcast(reals, x)


		"""
		urls = [i + '/kvs/' + key for i in memberslist]
		print memberslist
		print urls
		reals = [j.encode('ascii') for j in urls]
		print reals
		#the = jsonify(reals)
		#print the

		res = kvsput(key, x)
		member = reals.pop()

		try: 
			print member + " requester space\n"
			resp = requests.put(member, data = {'val':x}, timeout = 10)
			#'members':members
			return "titys!"
		except requests.exceptions.Timeout:
			#print members
			print "timedout\n"
			return "dick!"

		
		threads = []
		for a in reals:
		#while reals:
			#member = reals.pop()
			print  a + " while space\n"
			t = threading.Thread(target = requester, args = (a,))
				#kwargs = {'member':a, 'val': x})
				#args = (addr,))
			threads.append(t)
			t.start()
			"""
		#while threading.activeCount() > 1:
		#	pass
		#else:
		#	print "pass\n"
		#params = {'val':x}
		#rs = (grequests.put(t, data = {'val':x}) for t in reals)
		#the = grequests.map(rs)
		#for addr in memberslist:
			#multireq(addr, key, x)

		#res = requests.put(reals.pop(), data = {'val':x})

		#, hooks = {'pre_request': bcast(reals)})
		#kvsput(key, x, reals)
		#res.status_code

		return res
	elif request.method == 'DELETE':
		return kvsdel(key, x)
	else:
		return kvsget(key)

"""
def requester(member, val):
	print "entered requester\n"
	#with lock:
	#member = members.pop()
	#if not member:
	#	return
	#else:
	try: 
		print member + " requester space\n"
		res = requests.put(member, data = {'val':val}, timeout = 5)
		#'members':members
		return res.status_code
	except requests.exceptions.Timeout:
		#print members
		print "timedout\n"
		return
#def request_prepare(members)

@app.route('/mem')
def mem():
	return json.dumps(memberslistIds)
	#for z in memberslistIds:
	#	return z
	

def nodeputb(key, x):
	f = str(key)
 	for z in memberslistIds:
 		a = int(z)
		b = a +5
		c = str(b)
 		req = requests.put('http://10.0.0.2' + z + ':1234' + c + '/kvs/' + f, data = {'val':x})
 		if req.status_code!=(200 or 201):
 			return req.status_code
 		else:
 			return 'Success'

	
def nodekvsput(key, x):
	f = str(key)

	a = int(masternode)
	b = a +5
	c = str(b)

	r = requests.put('http://10.0.0.2'+ masternode + ':1234' + c + '/kvs/' + f, data = {'val':x})
	if r.status_code !=(200 or 201):
		return r.status_code
	else:
		return 'Success'


# request help function
def multireq(addr, key, val):
	print addr + '/kvs/' + key
	response = grequests.put(addr + '/kvs/' + key, data = {'val':val})
	return response
"""

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
			response.status_code = 200
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
		data = {
		'replaced' : 0,
		'msg' : 'success',
		'membersIDS': memberslistIds,
		'master':masternode
		}
		response = jsonify(data)
		response.status_code = 201
		return response

		#replace value of key with new value	
	else:
		kvs[key] = x
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


if __name__ == '__main__':
	app.debug = True
	app.run(host=ip, port=int(port))



