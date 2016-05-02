import requests
from . import _DB
from . import _Constants
from json import dumps
from flask import render_template, redirect, url_for

def catalogs(session):
	conn = requests.get(_Constants.PAYBOOK_LINK + 'catalogues/sites', params = {"token": session['token']})
	print(_Constants.INDENT,"CATALOGS")
	print(_Constants.INDENT,conn.status_code)
	print(_Constants.INDENT,conn.url)	
	session['catalog'] = conn.json()['response']
	accounts_registred = _DB.get_accounts(session['id_user_db'])		
	return render_template('catalogs.html', dicc = conn.json()['response'], accounts = accounts_registred, err = None)	

def credentials(session, data, institution):
	conn = requests.post(_Constants.PAYBOOK_LINK + 'credentials', data = dumps(data))
	print(_Constants.INDENT,"CREDENTIALS")	
	print(_Constants.INDENT,conn.status_code)
	print(_Constants.INDENT,conn.url)
	print(data)
	if conn.status_code == 200:
		data['OwnerId'] = session['id_user_db']
		data['name'] = institution
		data['data'] = conn.json()['response']
		data.pop('token',None)
		if _DB.account_exists(data['OwnerId'], data['name']):
			_DB.modify_credentials_in_db(data)
			print(_Constants.INDENT,"Account Modifided")
		else:
			_DB.accounts.insert_one(data)
			print(_Constants.INDENT,"Account created")					
		return dumps(conn.json())

def sync_account(response, data):
	headers = {'Content-type' : 'application/json'}	
	print(_Constants.INDENT, response['institution'])
	token_json_form = {}
	token_json_form['token'] = data['token']
	conn = requests.post(response['twofa'],headers=headers, data = dumps(data))
	status = requests.get(response['status'], params = token_json_form)
	accounts = requests.get(_Constants.PAYBOOK_LINK + 'accounts', params = token_json_form)
	count = requests.get(_Constants.PAYBOOK_LINK + 'attachments/count', params = token_json_form)
	attachments = requests.get(_Constants.PAYBOOK_LINK + 'attachments', params = token_json_form)
	print(_Constants.INDENT, "SYNC:________")
	print(_Constants.INDENT, conn.url)
	print(_Constants.INDENT, conn.status_code)
	print(_Constants.INDENT, conn.json())
	print(_Constants.INDENT, "STATUS:______")
	print(_Constants.INDENT, status.url)
	print(_Constants.INDENT, status.status_code)
	print(_Constants.INDENT, status.json())
	print(_Constants.INDENT, "ACCOUNTS:______")
	print(_Constants.INDENT, accounts.url)
	print(_Constants.INDENT, accounts.status_code)
	print(_Constants.INDENT, accounts.json())
	print(_Constants.INDENT, "COUNT:______")
	print(_Constants.INDENT, count.url)
	print(_Constants.INDENT, count.status_code)
	print(_Constants.INDENT, count.json())
	print(_Constants.INDENT, "ATTACHMENTS:______")
	print(_Constants.INDENT, attachments.url)
	print(_Constants.INDENT, attachments.status_code)
	print(_Constants.INDENT, attachments.json())

	if conn.status_code == 200 or status.status_code == 200:
		print(">>>>>>>>>>>>>>>>>>>200_CONN<<<<<<<<<<<<<<<<<<<<<<<<<<<")
		return dumps(accounts.json())
	else:
		print("--------------------------NO_CONN---------------------")	
		return dumps(status.json())

def login(session, email, api_key, id_user):
	conn = requests.post(_Constants.PAYBOOK_LINK + 'sessions', data = {"api_key": api_key, "id_user": id_user})
	print(_Constants.INDENT,"LOGIN")
	print(_Constants.INDENT,conn.status_code)
	print(_Constants.INDENT,conn.url)
	if conn.status_code == 200:
		session['username'] = email
		session['token'] = conn.json()['response']['token']		
		return redirect(url_for('catalogs'))
	else:
		return render_template('login.html', err = "Usuario o contraseña incorrectos")

def signup():
	conn = requests.post(_Constants.PAYBOOK_LINK + 'users', data = {"api_key":"95742121cd6005399898c014a21fe785", "name":"donmikeazul@hotmail.com"})
	print(_Constants.INDENT,"SINGUP")
	print(conn.status_code)
	print(conn.url)
	return conn

def widget():
	pass