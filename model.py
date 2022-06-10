from peewee import *
import datetime

db = SqliteDatabase('database.db')

class User(Model):
	name = CharField()
	about = TextField()

	class Meta:
		database = db

#User.create(name = '', about = '')

def initialize_db():
	db.connect()
	db.create_tables([User], safe = True)

initialize_db()
