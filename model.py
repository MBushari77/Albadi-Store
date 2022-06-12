from peewee import *
import datetime

db = SqliteDatabase('database.db')

class User(Model):
	username = CharField()
	name = CharField()
	# about = TextField()
	password = CharField()


	class Meta:
		database = db

#User.create(name = '', name = '', password='')

def initialize_db():
	db.connect()
	db.create_tables([User], safe = True)

initialize_db()
