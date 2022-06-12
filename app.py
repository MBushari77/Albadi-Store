from flask import Flask, render_template, request, redirect, url_for, make_response
from model import *
# from dbf import *

app = Flask(__name__)

def func():
	response = make_response( render_template() )
	response.set_cookie( "name", "value" )
	return response

def getCookie(cookie):
	key = request.cookies.get(cookie)
	return str(key)

@app.route('/')
def index():
	return render_template('index.html')

# Login route
@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		user = False
		username = request.form['username']
		password = request.form['password']

		for u in User.select():
			if u.username == username and u.password == password:
				user = u
		if not user:
			return redirect(url_for('index'))
		response = make_response( redirect(url_for('home')) )
		response.set_cookie( "session", str(user.id) )
		return response
	else:
		pass

@app.route('/home')
def home():

	user = User.select().where(User.id == 1)
	return render_template('home.html', user=user)



# Store route
@app.route('/store')
def store():
	return render_template('store.html')





# Logout route



if __name__ == '__main__':
	app.run(port=5000, debug=True)
