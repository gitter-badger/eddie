from http.client import HTTPConnection
import json
from threading import Thread
from urllib.parse import urlencode
from time import sleep

from pychatbot.bot import Bot, command


def test_http_interface():
	
	class MyBot(Bot):
		def default_response(self, in_message):
			return in_message[::-1]
			
	bot = MyBot()
	bot.http_serve()
		
	test_messages = ["hello", "another message"]
	for tm in test_messages:
		conn = HTTPConnection("127.0.0.1:8000")
		conn.request("GET", "/process?"+urlencode({"in_message":tm}))
		r = conn.getresponse()
		assert r.status == 200
		ret = json.loads(r.read().decode())
		assert ret["out_message"] == tm[::-1]
		conn.close()
		
	bot.http_stop()


def test_http_command():
	
	class MyBot(Bot):
		def default_response(self, in_message):
			return in_message[::-1]
		
		@command
		def start(self):
			return "Welcome!"
	
	b = MyBot()
	b.http_serve()
		
	conn = HTTPConnection("127.0.0.1:8000")
	conn.request("GET", "/process?in_message=/start")
	r = conn.getresponse()
	assert r.status == 200
	ret = json.loads(r.read().decode())
	assert ret["out_message"] == "Welcome!"
	conn.close()
	
	b.http_stop()