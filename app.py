from flask import Flask, render_template, request, redirect, url_for, make_response
from model import *
from flask_cors import CORS
import datetime as dt
# from dbf import *

app = Flask(__name__)
CORS(app)

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

"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
@app.route('/home')
def home():

	user = User.select().where(User.id == 1)
	return render_template('home.html', user=user)


"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
# Deal route
@app.route('/deal')
def deal():
	products = Product.select()
	return render_template('deal.html', products=products)

@app.route('/dothedeal', methods=['GET', 'POST'])
def dothedeal():
	if request.method == 'POST':
		data = request.json['data']
		print(data)
		return True
		


"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
# Pils route
@app.route('/pills')
def pills():
	return render_template('pills.html')

@app.route('/paid')
def paid():
	return render_template('paid.html')

@app.route('/waiting')
def waiting():
	return render_template('waiting.html')


"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
# Cuts route
@app.route('/cuts', methods=['GET', 'POST'])
def cuts():
	datentime = str(dt.datetime.now())[0:10]
	year = str(dt.datetime.now())[0:4]
	month = str(dt.datetime.now())[5:7]
	if request.method == 'POST':
		print('inside method post')
		datentime = request.form['datentime']
		print(datentime)
		year = datentime[0:4]
		month = datentime[5:7]
	print(year, month)
	cuts = Cut.select().where((Cut.year == year) and  (Cut.month == month))
	print(cuts)
	return render_template('cuts.html', cuts=cuts, datentime=datentime)

# New cut
@app.route('/newcut')
def newcut():
	return render_template('newcut.html')

@app.route('/addnewcut', methods=['GET', 'POST'])
def addnewcut():
	if request.method == 'POST':
		title = request.form['title']
		price = request.form['price']
		Cut.create(
			title=title,
			price=price,
			date=str(dt.datetime.now())[0:10],
			time=str(dt.datetime.now())[11:16],
			month=str(dt.datetime.now())[5: 7],
			year=str(dt.datetime.now())[0:4]
		)
		return redirect(url_for('cuts'))

# Delete a Cut 
@app.route('/deletecut/<int:id>')
def deletecut(id):
	Cut.delete().where(Cut.id == id).execute();
	return redirect(url_for('cuts'))





"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
# Store route
@app.route('/store')
def store():
	products = Product.select()
	return render_template('store.html', products=products)

# New product route
@app.route('/newproduct')
def newproduct():
	return render_template('newproduct.html')

@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
	if request.method == 'POST':
		name = request.form['name']
		price = request.form['price']
		mount = request.form['mount']
		Product.create(
			name=name,
			price=price,
			mount=mount,
			date=str(datetime.datetime.now())[0:16]
		)
		return redirect(url_for('store'))

# Delete a Product from the store
@app.route('/deleteproduct/<int:id>')
def deleteProduct(id):
	Product.delete().where(Product.id == id).execute();
	return redirect(url_for('store'))




# Logout route
@app.route('/logout')
def logout():
	return 'Loged out'


if __name__ == '__main__':
	app.run(port=5000, debug=True)
