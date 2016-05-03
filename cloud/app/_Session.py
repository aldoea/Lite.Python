# -​*- coding: utf-8 -*​-import os
from ..dependencies import _DB
from ..dependencies import _Constants
from ..dependencies import _Paybook
import datetime
import requests
from flask import render_template, redirect, url_for


def index(session):
	if 'username' in session:
		return render_template('index.html', session = session['username'])		
	return render_template('index.html', session = None)

def login(session, request):
	if request.method == 'POST':
		##########################################PAYBOOK CREDENTIALS ########################????????
		api_key = "95742121cd6005399898c014a21fe785"
		id_user = "5717b9b50c212a1d628b4568"
		email = request.values['email']
		psw = request.values['password']
		if _DB.log_in(session,email,psw):
			return _Paybook.login(session, email, api_key, id_user)
		else:
			return render_template('login.html', err = "Usuario o contraseña incorrectos")
	else:
		return render_template('login.html', err = None)

def signup(request):
	if request.method == 'POST':		
		email = request.values['email']
		psw = request.values['password']
		user = {
			'user': email,
			'password':psw,
			'date': datetime.datetime.utcnow()			
		}
		if _DB.search_user_in_db(email):
			print(_Constants.INDENT, "Usuario Existente")
			return render_template('signup.html', err = "Usuario en uso")
		else:
			conn = _Paybook.signup()
			if conn.status_code == 200:
				_DB.users.insert_one(user)
				return redirect(url_for('login'))
			else:
				return render_template('signup.html', err = "Usuario no pudo ser creado")
	else:
		return render_template('signup.html', err = None)

def logout(session):
	if 'username' in session:		
		session.pop('username', None)
		session.pop('token', None)
		session.pop('id_user_db', None)
		session.pop('catalog', None)
		return redirect(url_for('login'))
	return redirect(url_for('index'))