import yamail
from nameko.rpc import rpc, RpcProxy

class SendEmail(object):
	name = "eamil"

	@rpc
	def send(self, to, subject, content):
		yag = yamail.SMTP("wanglm.mickel@gmail.com", "wlm19941118")
		yag.send(to=to.encode("utf-8"), subject=subject.encode("utf-8"),\
			contents=[content.encode("utf-8")])