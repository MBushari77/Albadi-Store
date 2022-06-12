from peewee import *
from model import *
# User.create(username = 'bushari', name = 'mohammed', password='123')
users = User.select()
for u in users:
	print(u.id)