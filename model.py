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

#User.create(name = '', name = '', password='')

def initialize_db():
	db.connect()
	db.create_tables([User, Product], safe = True)

initialize_db()
