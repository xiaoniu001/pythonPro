from tornado import websocket, ioloop, web, httpserver
from RfridReader import RfridReader, ascii_carid
import time
import json


class TagsHandler(websocket.WebSocketHandler):
	
	def initialize(self):
		self.serial = None
	
	def check_origin(self, origin):
		return True
	
	def open(self, *args, **kwargs):
		
		self.write_message(dict(errorcode="0000", message="websocket 服务端打开连接！"))
	
	def on_close(self):
		# self.write_message("we hava disconnection !!")
		self.close()
	
	def on_message(self, message):
		req = json.loads(message)
		
		if req['message'] == "openPort":
			try:
				self.serial = RfridReader(port=req["port"])
				self.write_message(dict(errorcode="0000", message="串口打开成功！"))
			except Exception as e:
				print(e)
				self.write_message(dict(errorcode="9999", message="串口打开异常！"))
		elif req['message'] == "connectReq":
			self.write_message(dict(errorcode="0000", message="websocket 客户端打开连接！"))
		elif req['message'] == "closePort":
			self.serial.serial.close()
			self.write_message(dict(errorcode="0000", message="串口关闭！！"))
		elif req['message'] == "testConnect":
			n = 1
			while n <= 3:
				if self.serial.send_led_Buzzer(req):
					self.write_message(dict(errorcode="0000", message="串口通讯测试成功！！！"))
					break
				else:
					n += 1
					self.write_message(dict(errorcode="9999", message="测试通讯失败{}次！！！".format(n)))
		elif req['message'] == "lookCard":
			n = 1
			while n <= 3:
				rec_data = self.serial.get_card()
				if rec_data['errorcode'] == "03":
					self.write_message(rec_data)
					break
				else:
					n += 1
					self.serial.close_card()
					self.write_message(rec_data)
				time.sleep(0.5)
		elif req['message'] == "readBlock":
			start_block = req["start_block"]
			end_block = req["end_block"]
			for i in range(int(start_block), int(end_block) + 1):
				self.write_message(self.serial.read_card_nfc(i))
				time.sleep(2)
				
		elif req['message'] == "initCard":
			function_code = req["functionCode"]
			project_code = req["projectCode"]
			if project_code == "CCST":
				if function_code == "01" or function_code == "02":
					for i in [41, 42, 43]:
						if i == 41:
							self.write_message(self.serial.write_card(i, "00000004"))
						elif i == 42:
							self.write_message(self.serial.write_card(i, "1b000000"))
						else:
							self.write_message(self.serial.write_card(i, "5536314f"))
				else:
					self.write_message("项目功能码只支持01或02！")
			else:
				for i in [41, 42, 43]:
					if i == 41:
						self.write_message(self.serial.write_card(i, "00000004"))
					elif i == 42:
						self.write_message(self.serial.write_card(i, "1b000000"))
					else:
						self.write_message(self.serial.write_card(i, "ffffffff"))
				
		elif req["message"] == "writeBlock":
			
			start_block = req["start_block"]
			end_block = req['end_block']
			value = req["value"]
			mode = req["mode"]
			function_code = req["functionCode"]
			project_code = req["projectCode"]
			
			if project_code == "CCST" and function_code in ["01", "02"]:
				pwd = "5536314f"
			else:
				pwd = "ffffffff"
			print(function_code, project_code, pwd)
			pwd_res = self.serial.check_pwd(pwd)
		
			if pwd_res['errorcode'] == "0000":
				print("验证密码成功！")
				if mode == "0":
					n = 0
					for i in range(int(start_block), int(end_block) + 1):
						self.write_message(self.serial.write_card(i, value[n]))
						n += 1
						time.sleep(1)
				else:
					n = 0
					for i in range(int(start_block), int(end_block) + 1):
						self.write_message(self.serial.write_card(i, ascii_carid(value[n])))
						n += 1
						time.sleep(1)
			else:
				print("验证密码失败！请检测是否初始化nfc卡")
				self.write_message(pwd_res)
			self.serial.close_card()


if __name__ == '__main__':
	webapp = web.Application(
		handlers=[
			(r'/websocket', TagsHandler),
		],
		debug=False,
	)
	http_server = httpserver.HTTPServer(webapp)
	http_server.listen(8003)
	ioloop.IOLoop.instance().start()
