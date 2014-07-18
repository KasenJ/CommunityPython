'''Yeqin Zheng, 09/07/2014'''
import tornado.ioloop
import tornado.web
import tornado.httpserver
import json

''' Add a helper to an event. Succeed with "1" returned, else with "0". '''

class AddaidHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>AddaidHandler</p><form action='/api/addaid' method='post'><input type='submit' value='submit'></form>")
	def post(self):
		#content =self.request.body
		content = '{"username":"test1","eventid":"4"}'
		j = json.loads(content)

		result = self.application.dbapi.addaidhelper(j['username'], j['eventid'])
		self.write("{'state': " + result + "}")
