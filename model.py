from peewee import *
import datetime

db = SqliteDatabase('database.db')


class User(Model):
	username = CharField()
	name = CharField()
	password = CharField()
	# about = TextField()


	class Meta:
		database = db

# Products model
class Product(Model):
	name = CharField()
	price = IntegerField()
	mount = IntegerField()
	date = CharField()


	class Meta:
		database = db


# Cuts model
class Cut(Model):
	title = CharField()
	price = IntegerField()
	date = CharField()
	month = CharField()
	year = CharField()
	time = CharField()


	class Meta:
		database = db

#User.create(name = '', name = '', password='')

def initialize_db():
	db.connect()
	db.create_tables([User, Product, Cut], safe = True)

initialize_db()
