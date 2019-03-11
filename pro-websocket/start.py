from tornado import websocket, ioloop, web, httpserver
from RfridReader import RfridReader
import time
import json
import threading


class TagsHandler(websocket.WebSocketHandler):
	
	def initialize(self):
		self.serial = None
	
	def check_origin(self, origin):
		return True
	
	def open(self, *args, **kwargs):
		print("websocket 正在打开连接！")
		self.write_message("websocket 服务端打开连接！")
	
	def on_close(self):
		# self.write_message("we hava disconnection !!")
		self.close()
	
	def look_card(self):
		n = 1
		while n <= 3:
			rec_data = self.serial.get_card()
			if rec_data:
				# self.write_message(rec_data["message"])
				return rec_data
			else:
				n += 1
				self.serial.close_card()
			time.sleep(0.02)
		return False
	
	def write_card(self, value):
		is_success = True
		for i in value["block"]:
			if self.serial.write_card(i, value["value"][value["block"].index(i)]):
				time.sleep(0.02)
				continue
			else:
				is_success = False
				break
		if is_success:
			print("写入数据成功！")
			self.write_message("写入数据成功！")
			self.serial.close_card()
		else:
			print("写入数据失败！")
			self.write_message("写入数据失败！")
			self.serial.close_card()
	
	def on_message(self, message):
		req = json.loads(message)
		print("收到请求", req['message'])
		if req['message'] == "openPort":
			try:
				self.serial = RfridReader(port=req["port"])
				self.write_message("串口打开成功！")
			except Exception as e:
				print(e)
				self.write_message("串口打开异常！")
		elif req['message'] == "connectReq":
			self.write_message("websocket 客户端打开连接！")
		elif req['message'] == "closePort":
			self.serial.serial.close()
		# self.write_message("串口关闭! ")
		elif req['message'] == "testConnect":
			n = 1
			while n <= 3:
				if self.serial.send_led_Buzzer(req):
					self.write_message("测试通讯成功!")
					break
				else:
					n += 1
			if n > 3:
				self.write_message("测试通讯失败！")
		elif req['message'] == "lookCard":
			n = 1
			while n <= 3:
				start = time.clock()
				rec_data = self.serial.get_card()
				print("寻卡接收数据", rec_data)
				if rec_data:
					# self.write_message(rec_data["message"])
					self.write_message(rec_data)
					# self.serial.close_card()
					break
				else:
					n += 1
					print("寻卡返回时间", time.clock() - start)
			# self.serial.close_card()
			if n > 3:
				self.write_message("检测区无卡！")
		
		# print("寻卡开始时间", time.clock()-start)
		# n = 1
		# while n <= 3:
		# 	rec_data = self.serial.get_card()
		# 	if rec_data['errorcode'] == "03":
		# 		self.write_message(rec_data["message"])
		# 		break
		# 	else:
		# 		n += 1
		# 		self.serial.close_card()
		# 	time.sleep(0.1)
		
		elif req['message'] == "readBlock":
			start_block = req["start_block"]
			end_block = req["end_block"]
			for i in range(int(start_block), int(end_block) + 1):
				self.write_message(self.serial.read_card_nfc(i))
				time.sleep(0.1)
		
		elif req['message'] == "initCard":
			pwd_li = ['5536314f', 'ffffffff', '85544979']
			for i in pwd_li:
				self.serial.get_card()
				pwd_res = self.serial.check_pwd(i)
				
				if pwd_res['errorcode'] == "0000":
					print("{}密码验证成功！".format(i))
					self.write_message("{}密码验证成功！".format(i))
					
					if i != '85544979':
						for j in [41, 42, 43]:
							if j == 41:
								if self.serial.write_card(j, "00000004"):
									print("写41块成功！")
							elif j == 42:
								if self.serial.write_card(j, "1b000000"):
									print("写42块成功！")
							else:
								if self.serial.write_card(j, "85544979"):
									print("写43块成功！")
								
						self.serial.close_card()
						break
					else:
						self.write_message("密码已初始化为85544979")
						break
		
		elif req["message"] == "writeBlock":
			
			value = req["value"]
			print("写卡数据{}".format(value))
			function_code = req["functionCode"]
			project_code = req["projectCode"]
			if project_code == "CCST" and function_code in ["01", "02"]:
				
				for i in ['5536314f', 'ffffffff', '85544979']:
					self.serial.get_card()
					pwd_res = self.serial.check_pwd(i)
					if pwd_res['errorcode'] == "0000":
						card_pwd = True
						print("{}密码验证成功！".format(i))
						if i != '85544979':
							for j in [41, 42, 43]:
								if j == 41:
									if self.serial.write_card(j, "00000004"):
										print("写41块失败！")
								elif j == 42:
									if self.serial.write_card(j, "1b000000"):
										print("写42块失败！")
								else:
									if self.serial.write_card(j, "85544979"):
										print("写43块失败！")
							print("密码已初始化为85544979")
							self.write_card(value)
							break
						else:
							print("密码已初始化为85544979")
							self.write_card(value)
							break
					else:
						continue
				if not card_pwd:
					for j in [41, 42, 43]:
						if j == 41:
							self.write_message(self.serial.write_card(j, "00000004"))
						elif j == 42:
							self.write_message(self.serial.write_card(j, "1b000000"))
						else:
							self.write_message(self.serial.write_card(j, "85544979"))
					print("密码已初始化为85544979")
					self.write_card(value)
					
			else:
				pass


if __name__ == '__main__':
	webapp = web.Application(
		handlers=[
			(r'/websocket', TagsHandler),
		],
		debug=False,
	)
	http_server = httpserver.HTTPServer(webapp)
	http_server.listen(5003)
	ioloop.IOLoop.instance().start()
