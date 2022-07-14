from peewee import *
import datetime
import json

class JSONField(TextField):
	def db_value(self, value):
		return json.dumps(value)

	def python_value(self, value):
		if value is not None:
			return json.loads(value)



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

class Pill(Model):
	customerName = CharField()
	data = JSONField()
	price = IntegerField()
	month = CharField()
	year = CharField()
	date = CharField()
	status = BooleanField(default=False)
	
	class Meta:
		database = db


def initialize_db():
	db.connect()
	db.create_tables([User, Product, Cut, Pill], safe = True)

initialize_db()
