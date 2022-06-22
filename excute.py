from peewee import *
from model import *
# User.create(username = 'bushari', name = 'mohammed', password='123')
users = Product.select()
for u in users:
	print(u.name)
	print(u.price)
	print(u.date)
	print('___________')