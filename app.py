from flask import Flask, render_template, request, redirect, url_for
from model import *
# from dbf import *

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(port=5000, debug=True)
