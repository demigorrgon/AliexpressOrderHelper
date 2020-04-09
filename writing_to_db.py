import os
import sqlite3
from AliexpressOrdersAutomation.AliexpressOrderHelper.ali_login import Aliexpress
from selenium import webdriver

# checking if db exists and creating db file if doesn't
try:
	os.mknod('AliexpressOrderData.db')
	print('Db created')
except FileExistsError:
	print('Db file exists')

# TODO: Wrap all sensitive variables in 'try: except:'
conn = sqlite3.connect('AliexpressOrderData.db')

c = conn.cursor()
# make if statement that checks if db was not created,then creates it or pass
try:
	c.execute('''
		SELECT * FROM OrderData
	''')
except sqlite3.OperationalError:
	c.execute(
		'''
		CREATE TABLE OrderData
		(id INTEGER PRIMARY KEY,
		order_number INTEGER,
		time_of_order DATE,
		order_price INTEGER,
		dispute BOOLEAN
		);''')
	print('Table was created')

# insert your account information here:
# You need to install geckodriver first: for Firefox: https://github.com/mozilla/geckodriver
get_information = Aliexpress(
	driver=webdriver.Firefox(), login='', password=''
).getting_orders()

info = [item for item in get_information]
# print(info)
ids = info[0::3]
time = info[1::3]
price = info[2::3]
prepare_to_write = list(zip(ids, time, price))
for item_ids, order_date, order_prices in prepare_to_write:
	c.execute(
		'INSERT INTO OrderData(order_number, time_of_order, order_price) VALUES (?, ?, ?)', (
			item_ids, order_date, order_prices))
# TODO: Add dispute column; It should be true or false, depending at status of dispute in the 'My orders' page

conn.commit()
for row in c.execute('SELECT * FROM Orderdata'):
	print(row)

# TODO: Add option to check multiple accounts via reading from a file
get_information.close()
conn.close()

