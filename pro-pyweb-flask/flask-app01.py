from flask import Flask, render_template, jsonify, redirect, url_for
from flask import request, render_template

app = Flask(__name__)

@app.route('/hello')
def hello_word():
	return "Hello World"

@app.route('/user/', methods=['GET','POST'])
@app.route('/user/<string:username>')
def get_user(username=None):
	info = None
	if request.method == "GET":
		if username:
			return username
		else:
			return render_template("login.html", info = {"status":200, "result":"login"})
	return username

@app.route('/user/<user_id>', methods=['GET','POST'])
def get_user_id(user_id):
	return user_id


if __name__ == '__main__':
	# debug=True: support the server will reload itself on code change
	# and provide you with a helpful debugger if things go wrong 
	app.run(debug=True)
