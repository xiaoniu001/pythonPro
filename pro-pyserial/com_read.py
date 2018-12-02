import serial
from config import *
from functools import reduce


def read_data():
	"""
	读取数据
	:return:
	"""
	with serial.Serial(port=PORT, baudrate=BAUD_RATE, timeout=TIMEOUT) as ser:
		# while True:
		# 		# 	print(ser.read(20))
		bytes_str = bytes().fromhex('AAFFB0030A050AE3')
		print(bytes_str)
		N = ser.write(bytes_str)
		print(ser.read(N))


def bcc(hex_str):
	"""
	bcc加密字符串
	:param hex_str: 需要加密的十六进制字符串
	:return:
	"""
	bcc_code = reduce(lambda x, y: int(str(x), 16) ^ int(str(y), 16), hex_str.split(" "))
	# bcc_code = reduce(lambda x, y: print(x, y), [1, 2, 5, 8])
	print(bcc_code)


if __name__ == '__main__':
	st = "AA FF B0 03 0A 05 0A E3"
	bcc('AA FF B0')
	# print('AA FF B0 03 0A 05 0A'.split(" "))
