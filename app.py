from flask import Flask, render_template, request, redirect, url_for, make_response, session, jsonify
from model import *
import datetime as dt
# from dbf import *

import os


app = Flask(__name__)
app.secret_key = os.urandom(25)


def func():
	response = make_response( render_template() )
	response.set_cookie( "name", "value" )
	return response

def isLogedIn():
	try:
		cookie = session['session']
		print(cookie)
		if int(cookie) > 0:
			return True
		else:
			return False
	except:
		return False

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
		session['session'] = user.id
		return redirect(url_for('home'))
	else:
		pass

"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
@app.route('/home')
def home():
	if not isLogedIn():
		return redirect(url_for('index'))


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
	if not isLogedIn():
		return redirect(url_for('index'))

	products = Product.select()
	return render_template('deal.html', products=products)

@app.route('/dothedeal', methods=['GET', 'POST'])
def dothedeal():
	if not isLogedIn():
		return redirect(url_for('index'))

	if request.method == 'POST':
		data = request.get_json(force=True)
		# print("data ###########################################")
		customerName = data[0]['name']
		price = 0
		for i in data[1:]:
			price += i['price'] * i['mount']
		Pill.create(
			customerName = customerName,
			data = data[1:],
			price = price,
			month = str(dt.datetime.now())[5:7],
			year = str(dt.datetime.now())[0:4],
			date = str(dt.datetime.now())[0:10],
		)

		for pro in data[1:]:
			try:
				productToEdit = Product.select().where(Product.id == pro['id']).get()
				productToEdit.mount -= pro['mount']
				productToEdit.save()
			except:
				print('continue')

		# print("data ###########################################")
		return jsonify({'success': True})
		


"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
# Pils route
@app.route('/pills')
def pills():
	if not isLogedIn():
		return redirect(url_for('index'))

	return render_template('pills.html')

@app.route('/waiting', methods = ['GET', 'POST'])
def waiting():
	if not isLogedIn():
		return redirect(url_for('index'))

	datentime = str(dt.datetime.now())[0:10]
	year = str(dt.datetime.now())[0:4]
	month = str(dt.datetime.now())[5:7]
	if request.method == 'POST':
		datentime = request.form['datentime']
		year = datentime[0:4]
		month = datentime[5:7]

	unpaidPills = Pill.select().where((Pill.month == month) & (Pill.year == year) & (Pill.status == False))

	return render_template('waiting.html', pills=unpaidPills, datentime = datentime)

@app.route('/paid', methods = ['GET', 'POST'])
def paid():
	if not isLogedIn():
		return redirect(url_for('index'))

	datentime = str(dt.datetime.now())[0:10]
	year = str(dt.datetime.now())[0:4]
	month = str(dt.datetime.now())[5:7]
	if request.method == 'POST':
		datentime = request.form['datentime']
		year = datentime[0:4]
		month = datentime[5:7]

	paidPills = Pill.select().where((Pill.month == month) & (Pill.year == year) & (Pill.status == True))

	return render_template('paid.html', pills=paidPills, datentime = datentime)


@app.route('/deletepill/<int:id>')
def deletepill(id):
	if not isLogedIn():
		return redirect(url_for('index'))

	pill = Pill.select().where(Pill.id == id)

	for i in pill:
		for pro in i.data:
			try:
				print(pro)
				productToEdit = Product.select().where(Product.id == pro['id']).get()
				productToEdit.mount += pro['mount']
				productToEdit.save()
			except:
				continue
	Pill.delete().where(Pill.id == id).execute();

	return redirect(url_for('pills'))

@app.route('/showpill/<int:id>')
def showpill(id):
	if not isLogedIn():
		return redirect(url_for('index'))

	pill = Pill.select().where(Pill.id == id)
	return render_template('showpill.html', pill = pill)

@app.route('/editpill/<int:id>')
def editpill(id):
	if not isLogedIn():
		return redirect(url_for('index'))

	pill = Pill.select().where(Pill.id == id)
	return render_template('editpill.html', pill = pill)


@app.route('/pillpaid/<int:id>')
def pillpaid(id):
	if not isLogedIn():
		return redirect(url_for('index'))

	pill = Pill.select().where(Pill.id == id).get()
	pill.status = True
	pill.save()
	return redirect(url_for('pills'))




"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
# Cuts route
@app.route('/cuts', methods=['GET', 'POST'])
def cuts():
	if not isLogedIn():
		return redirect(url_for('index'))

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
	cuts = Cut.select().where((Cut.year == year) &  (Cut.month == month))
	print(cuts)
	return render_template('cuts.html', cuts=cuts, datentime=datentime)

# New cut
@app.route('/newcut')
def newcut():
	if not isLogedIn():
		return redirect(url_for('index'))

	return render_template('newcut.html')

@app.route('/addnewcut', methods=['GET', 'POST'])
def addnewcut():
	if not isLogedIn():
		return redirect(url_for('index'))

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
	if not isLogedIn():
		return redirect(url_for('index'))

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
	if not isLogedIn():
		return redirect(url_for('index'))

	products = Product.select()
	return render_template('store.html', products=products)

# New product route
@app.route('/newproduct')
def newproduct():
	if not isLogedIn():
		return redirect(url_for('index'))

	return render_template('newproduct.html')

@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
	if not isLogedIn():
		return redirect(url_for('index'))

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

@app.route('/updateproduct', methods=['GET', 'POST'])
def updateproduct():
	if not isLogedIn():
		return redirect(url_for('index'))

	if request.method == 'POST':
		proId = request.form['id']
		name = request.form['name']
		price = request.form['price']
		mount = request.form['mount']
		product = Product.select().where(Product.id == int(proId)).get()
		product.name = name
		product.price = int(price)
		product.mount = int(mount)
		product.save()
		return redirect(url_for('store'))

@app.route('/editproduct/<int:id>')
def editproduct(id):
	if not isLogedIn():
		return redirect(url_for('index'))

	product = Product.select().where(Product.id == id)
	return render_template('editproduct.html', product=product)

# Delete a Product from the store
@app.route('/deleteproduct/<int:id>')
def deleteProduct(id):
	if not isLogedIn():
		return redirect(url_for('index'))

	Product.delete().where(Product.id == id).execute();
	return redirect(url_for('store'))

@app.route('/counts', methods=['GET', 'POST'])
def counts():
	if not isLogedIn():
		return redirect(url_for('index'))

	datentime = str(dt.datetime.now())[0:10]
	year = str(dt.datetime.now())[0:4]
	month = str(dt.datetime.now())[5:7]
	if request.method == 'POST':
		print('inside method post')
		datentime = request.form['datentime']
		print(datentime)
		year = datentime[0:4]
		month = datentime[5:7]
	# Count the in come from the pills
	incomeThisMonth = 0
	pills = Pill.select().where((Pill.status == True) & (Pill.month == month) & (Pill.year == year))
	for pill in pills:
		# print(pill.customerName)
		incomeThisMonth += pill.price
		# for product in pill.data:
		# 	incomeThisMonth += (product['price'] * product['mount'])
	# Count the cuts of this mounth
	cutsThisMounth = 0
	cuts = Cut.select().where((Cut.month == month) & (Cut.year == year))
	for cut in cuts:
		cutsThisMounth += cut.price
	print('cutsThisMounth', cutsThisMounth)

	# count total
	total = incomeThisMonth - cutsThisMounth
	return render_template('counts.html', income=incomeThisMonth, datentime=datentime, cuts=cutsThisMounth, total=total)















@app.route('/updatepill', methods=['GET', 'POST'])
def updatepill():
	if not isLogedIn():
		return redirect(url_for('index'))

	if request.method == 'POST':
		data = request.get_json(force=True)
		# print(data)

		pillId = data[0]['pillid']
		price = 0
		newData = data[1:]
		pill = Pill.select().where(Pill.id == pillId).get()
		# print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
		oldData = pill.data



		for i in range(len(newData)):
			price += newData[i]['price'] * newData[i]['mount']
			newData[i]['name'] = oldData[i]['name']

		# print(oldData)
		pill.data = newData
		pill.price = price
		pill.save()
		# UPDATE THE PRODUCTS IN THE STORE
		for i in range(len(newData)):
			# print(oldData[i], newData[i])
			try:
				productToEdit = Product.select().where(Product.id == oldData[i]['id']).get()

				productToEdit.mount += oldData[i]['mount'] - newData[i]['mount']
				# print('dif', oldData[i]['id'] - newData[i]['id'])
				productToEdit.save()
			except:
				print('continue')
		# print("data ###########################################")
		return jsonify({'success': True})







@app.route('/paidproducts/<int:productID>', methods=['GET', 'POST'])
def paidproducts(productID):	
	if not isLogedIn():
		return redirect(url_for('index'))

	datentime = str(dt.datetime.now())[0:10]
	year = str(dt.datetime.now())[0:4]
	month = str(dt.datetime.now())[5:7]
	if request.method == 'POST':
		datentime = request.form['datentime']
		year = datentime[0:4]
		month = datentime[5:7]

	name = ''
	mount = 0
	pills = Pill.select().where((Pill.month == month) & (Pill.year == year) & (Pill.status == True))

	for pill in pills:
		for product in pill.data:
			if product['id'] == productID:
				mount += product['mount']
				name = product['name']

	return render_template('paidproducts.html', name=name, mount=mount, datentime=datentime, productID=productID)








# Logout route
@app.route('/logout')
def logout():
	del session['session']
	return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(port=5000, debug=True)
