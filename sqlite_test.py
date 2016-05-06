import sqlite3
from json import dumps

connection = sqlite3.connect(":memory:")
cur = connection.cursor()

# Create table
cur.execute('''CREATE TABLE users (username text, password text, id_user text, date text)''')
cur.execute(''' CREATE TABLE credentials (ownerId text, institution_name text, credentials text)''')

# Insert a row of data
def insert_data():	
	cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','MAC',100,35.14)")
	# Save (commit) the changes
	connection.commit()

# Get all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())

# Get Headers
def get_headers():
	cur.execute("PRAGMA table_info(stocks)")
	print(cur.fetchall())

# Do a consult
def get_row(pc_name):	
	pc = (pc_name,)
	cur.execute('SELECT * FROM stocks WHERE symbol=?', pc)
	print(cur.fetchone())
	#return cur.fetchone()

def modify_name(next_name, past_name):
	new_name = (next_name,)
	old_name = (past_name,)
	cur.execute('UPDATE stocks SET symbol=:new_name WHERE symbol=:old_name', {"new_name": next_name, "old_name": past_name})
	print(cur.fetchone())


def search_user():	
	cur.execute('SELECT * FROM users')
	user = cur.fetchall()
	print(user)	

def search_credentials():	
	cur.execute('SELECT * FROM credentials')
	user = cur.fetchall()
	print(user)	

def sqliter(string):
	return (string,)

def create_user(user):
	username = user['user']
	password = user['password']
	id_user = user['id_user']
	date = user['date']
	insert_user = [(username ,password ,id_user ,date),]
	cur.executemany('INSERT INTO users VALUES (?,?,?,?)', insert_user)
	# Save (commit) the changes
	connection.commit()

def create_credentials(data):
	ownerId = data['ownerId']
	institution_name = data['name']
	credentials = dumps(data['credentials'])
	insert_credentials = [(ownerId, institution_name, credentials),]
	cur.executemany('INSERT INTO credentials VALUES (?,?,?)', insert_credentials)
	connection.commit()


user = {}
user['user'] = "aldo.ea@hotline.com"
user['password'] = "99912929"
user['id_user'] = "knooip12jd12o2kdp3kdA"
user['date'] = "2016-06-06"
create_user(user)
search_user()

data = {}
data['ownerId'] = "knooip12jd12o2kdp3kdA"
data['name'] = "BANCO666"
data['credentials'] = {'RFC': "EOAA950602HM56", 'PSW': 'BIGd4t4'}
create_credentials(data)
search_credentials()

connection.close()