import serial
import binascii
import re
from functools import reduce

import time


def ascii_carid(carid):
	"""
	将字符串转为ascii 十六进制  "b9870" -> "4239383730"
	:param carid:
	:return:
	"""
	new_carid = ""
	for i in carid:
		new_carid += hex(ord(i))[2:]
	return new_carid


def xor(hex_str1, hex_str2):
	"""
	对两个十六进制参数进行异或
	:param hex_str1:
	:param hex_str2:
	:return:
	"""
	
	if isinstance(hex_str1, str):
		return int(str(hex_str1), 16) ^ int(str(hex_str2), 16)
	elif isinstance(hex_str1, int):
		return hex_str1 ^ int(str(hex_str2), 16)


def bcc(hex_str):
	"""
	bcc加密字符串
	:param hex_str: 需要加密的十六进制字符串
	:return: 返回校验码
	"""
	
	bcc_code = reduce(xor, hex_str.split(" "))
	if int(bcc_code) < 16:
		bcc_str = (hex_str + "0" + hex(bcc_code)[2:]).replace(" ", "")
		print(bcc_str)
		return bcc_str
	else:
		bcc_str = (hex_str + hex(bcc_code)[2:]).replace(" ", "")
		print(bcc_str)
		return bcc_str


def split_str(str_data):
	"""
	两个字符分割字符串,例如："ahdddd" -> "ah dd dd"
	:param str_data: 字符串
	:return:
	"""
	new_str = ""
	for i in range(0, len(str_data), 2):
		new_str += str_data[i:i + 2] + " "
	return new_str[:-1]


def check_hex(num):
	"""
	校验数字，如果小于16位，添加"0"
	:return:
	"""
	if num < 16:
		return "0" + hex(num)[2:]
	else:
		return hex(num)[2:]


class RfridReader(object):
	"""
	安全栓指令下发
	"""
	
	def __init__(self, port="COM3", baud_rate=115200, byte_size=8, stopbits=1):
		"""
		初始化打开串口，无关闭操作，关闭机制待完善
		:param port: 串口号
		:param baud_rate: 波特率
		"""
		self.port = port
		self.baud_rate = baud_rate
		
		self.serial = serial.Serial(port=port, baudrate=baud_rate, timeout=1, bytesize=byte_size, stopbits=stopbits)
	
	def check_serial(self):
		"""
		查询串口是否打开
		:return:
		"""
		if self.serial.is_open:
			return True
		else:
			return False
	
	def send_led_Buzzer(self, message):
		"""
		控制蜂鸣器和led指令, 测试通讯
		:return:
		"""
		time_light = int(int(message["time_light"]) / 10)
		voicetimes = int(int(message["voicetimes"]))
		voiceshut = int(int(message["voiceshut"]) / 10)
		voicesilent = int(int(message["voicesilent"]) / 10)
		sub_str = check_hex(voicetimes) + check_hex(voiceshut) + check_hex(voicesilent) + check_hex(time_light)
		hex_str = "aaffb0{}".format(sub_str)
		bytes_str = bytes().fromhex(bcc(split_str(hex_str)))
		try:
			self.serial.write(bytes_str)
			response = str(binascii.b2a_hex(self.serial.read(10)))[2:-1]
			if response:
				if response == "bbffb0f4" or response == "bbffbafe":
					return True
				else:
					print("蜂鸣器控制指令接收错误: ", response)
					return True
			else:
				print("蜂鸣器控制指令没有接收到返回数据")
				return False
		except Exception as e:
			print("控制蜂鸣器和led指令出错：", e)
			return False
	
	def receive_card(self):
		"""
		读卡器主动上传卡号
		:return:
		"""
		response = ""
		try:
			response = str(binascii.b2a_hex(self.serial.read(100)))[2:-1]
		except Exception as e:
			print("读取卡号错误", e)
		pattern_patrol = re.compile(r"bbff00.{10}", re.I)
		records = set(pattern_patrol.findall(response))
		return records
	
	def get_card(self):
		"""
		寻卡21u读卡器
		:return:
		"""
		hex_str = bytes().fromhex("aaff705277")
		try:
			start = time.clock()
			self.serial.write(hex_str)
			res = str(binascii.b2a_hex(self.serial.read(100)))[2:-1]
			print(time.clock()-start)
			if res == "bbffa0e4":
				return {"errorcode": "02", "message": "检测区无卡"}
			elif res[0:6] == "bbff77":
				return {"errorcode": "03", "message": "卡uid: {}".format(res[6:-2])}
			elif res[0:6] == "bbff70":
				return {"errorcode": "03", "message": "卡uid: {}".format(res[6:-2])}
			else:
				return {"errorcode": "02", "message": "检测区无卡"}
			
		except Exception as e:
			print("寻卡下发指令失败", e)
			return {"errorcode": "00", "message": "检测区无卡"}
	
	# def get_card(self):
	# 	"""
	# 	寻卡21u读卡器
	# 	:return:
	# 	"""
	# 	hex_str = bytes().fromhex("aaff705277")
	# 	try:
	# 		self.serial.write(hex_str)
	# 		res = str(binascii.b2a_hex(self.serial.read(100)))[2:-1]
	# 		if res:
	# 			if res == "bbffa0e4":
	# 				return "检测区无卡！"
	# 			elif res[0:6] == "bbff77":
	# 				return "卡uid: {}".format(res[6:-2])
	# 			elif res[0:6] == "bbff70":
	# 				return "卡uid: {}".format(res[6:-2])
	# 			else:
	# 				return "检测区无卡"
	# 		else:
	# 			print("寻卡未收到返回数据")
	# 			return "检测区无卡"
	# 	except Exception as e:
	# 		print("寻卡下发指令失败", e)
	# 		return "检测区无卡！"
	
	def close_card(self):
		"""
		关闭卡
		:return:
		"""
		hex_str = bytes().fromhex("aaff4015")
		try:
			self.serial.write(hex_str)
			time.sleep(1)
			return True
		except Exception as e:
			print("关卡下发指令失败！", e)
			return False
	
	def read_card_nfc(self, num):
		"""
		读nfc卡
		:return:
		"""
		hex_str = "aaff12{}".format(check_hex(num))
		
		try:
			
			self.serial.write(bytes().fromhex(bcc(split_str(hex_str))))
			res = str(binascii.b2a_hex(self.serial.read(100)))[2:-1]
			print("读卡返回数据：{}".format(res))
			if res == "bbffa0e4":
				return dict(message="读{0}块数据失败！".format(num))
			elif res[0:6] == "bbff12":
				return dict(message="读{0}块数据成功！{1}".format(num, res[6:14]))
			else:
				return dict(message="读卡数据失败！")
		
		except Exception as e:
			print(e)
			return "读卡数据失败！"
	
	def read_card_rfid(self, num, vftype):
		"""
		读取rfid卡
		:param num: 卡块号
		:param vftype: 密码类型
		:return:
		"""
		if vftype == "A":
			hex_str = "aaff10{num}60ffffffffffff".format(num=num)
			self.serial.write(bytes().fromhex(bcc(split_str(hex_str))))
			res = str(binascii.b2a_hex(self.serial.read(100)))[2:-1]
			print(res)
		elif vftype == 'B':
			pass
		else:
			pass
	
	def check_pwd(self, pwd):
		"""
		验证密码
		:return:
		"""
		hex_str = "aaff83{}".format(pwd)
		try:
			self.serial.write(bytes().fromhex(bcc(split_str(hex_str))))
			res = str(binascii.b2a_hex(self.serial.read(100)))[2:-1]
			print("验证{0}密码返回：{1}".format(pwd, res))
			if res == "bbffa0e4":
				return dict(errorcode="9999", message="验证密码失败！")
			elif res[0:6] == "bbff83":
				return dict(errorcode="0000", message="验证密码成功！")
			else:
				return dict(errorcode="9999", message="验证密码失败！")
		
		except Exception as e:
			print("nfc卡验证密码失败！！")
			return dict(errorcode="9999", message="验证密码失败！")
	
	def write_card(self, num, data):
		"""
		写nfc卡
		:param num: 块号
		:param data: 数据
		:return:
		"""
		if len(data) < 16:
			data += "0" * (32 - len(data))
		hex_str = "aaff22{0}{1}".format(check_hex(num), data)
		print(hex_str)
		try:
			self.serial.write(bytes().fromhex(bcc(split_str(hex_str))))
			res = str(binascii.b2a_hex(self.serial.read(100)))[2:-1]
			print("写卡返回数据：{}".format(res))
			if res == "bbffa0e4":
				return dict(errorcode="9999", message="写卡失败！")
			elif res[0:6] == "bbffaf":
				return dict(errorcode="0000", message="写卡第{}块成功！".format(num))
			else:
				return dict(errorcode="9999", message="写卡失败！")
		except Exception as e:
			print("写卡数据失败！")
			return dict(errorcode="9999", message="写卡失败！")
