#coding: utf-8
import yagmail


class Email(object):
	
	def __init__(self):
		self.eamil = "wanglm.mickel@gmail.com"
		self.password = "wlm19941118"


	def send(self, to, subject, content):
		yag = yagmail.SMTP(self.eamil, self.password)
		yag.send(to, subject,contents=[content])


if __name__ == '__main__':
	email = Email()
	email.send("wanglm.mickel@gmail.com", "Hello", "Hello Mickelwang !")