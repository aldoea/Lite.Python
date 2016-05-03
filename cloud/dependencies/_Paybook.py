# -​*- coding: utf-8 -*​-
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
	accounts_registred = {}	
	query = _DB.get_accounts(session['id_user_db'])
	if query is not None:
		for item in query:			
			accounts_registred[item['name']] = item['id_site']
	return render_template('catalogs.html', dicc = conn.json()['response'], accounts = accounts_registred)	

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

	#count = requests.get(_Constants.PAYBOOK_LINK + 'attachments/count', params = token_json_form)	
	#accounts = requests.get(_Constants.PAYBOOK_LINK + 'accounts', params = token_json_form)
	#attachments = requests.get(_Constants.PAYBOOK_LINK + 'attachments', params = token_json_form)
	#transactions = requests.get(_Constants.PAYBOOK_LINK + 'transactions', params = token_json_form)

	print(_Constants.INDENT, "SYNC:________")
	print(_Constants.INDENT, conn.url)
	print(_Constants.INDENT, conn.status_code)
	print(_Constants.INDENT, "STATUS:______")
	print(_Constants.INDENT, status.url)
	print(_Constants.INDENT, status.status_code)
	print(_Constants.INDENT, status.json())
	#print(_Constants.INDENT, conn.json())	
	return dumps(status.json())
	#print(_Constants.INDENT, status.json())	


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

def get_accounts(data):
	accounts = accounts = requests.get(_Constants.PAYBOOK_LINK + 'accounts', params = data)
	print(_Constants.INDENT, "ACCOUNTS:________")
	print(_Constants.INDENT, accounts.url)
	print(_Constants.INDENT, accounts.status_code)
	print(_Constants.INDENT, accounts.json())
	if accounts.status_code == 200:
		return render_template('accounts.html', data = accounts.json()['response'])
	else:
		return dumps({'Status':'Unsuccess'})

def get_transactions(data):
	transactions = requests.get(_Constants.PAYBOOK_LINK + 'transactions', params = data)
	print(_Constants.INDENT, "TRANSACTIONS:________")
	print(_Constants.INDENT, transactions.url)
	print(_Constants.INDENT, transactions.status_code)
	print(_Constants.INDENT, transactions.json())
	if transactions.status_code == 200:
		return render_template('transactions.html', data = transactions.json()['response'])
	else:
		return dumps({'Status':'Unsuccess'})	
