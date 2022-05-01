#!/user/bin/env python3
from scripts import database, handler
from flask import Flask, session, request
from flask_jwt_extended import create_access_token, JWTManager
from flask_cors import CORS, cross_origin
from werkzeug.exceptions import HTTPException
from datetime import timedelta
import json
import sys
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_POOL_RECYCLE'] = 28800 - 1
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 18000
app.config['JWT_SECRET_KEY'] = 'please-remember-to-change-me'
jwt = JWTManager(app)

#=============================RESPONSES====================================
HOMEPAGE = json.dumps({'render': 'home'})
WELCOME = json.dumps({'render': 'welcome'})
LOGIN = json.dumps({'render': 'login'})
SIGNUP = json.dumps({'render': 'signup'})
SIGNUP_ERROR = json.dumps({'error': 'signup_error'})
INVALID_CREDENTIALS = json.dumps({'error': 'invalid_credentials'})
USERNAME_ERROR = json.dumps({'error': 'username_unavailable'})
EMAIL_ERROR = json.dumps({'error': 'email_unavailable'})
PASSWORD_ERROR = json.dumps({'error': 'password_error'})
EMPTY_ERROR = json.dumps({'error': 'empty_fields'})

#==============================ACCESS-CONNECTIONS======================
tokens = []
users = []
# TODO Token refresh timer

#==============================AUTHENTICATION=========================
@app.route('/', methods=['POST'])
@cross_origin()
def welcome():
    access_token = request.json['access_token']
    for index, token in enumerate(tokens):
        if token == access_token:
            return json.dumps({'user_data': users[index]})
    return json.dumps({'error': 'invalid_token'})
    

#==============================LOGIN===================================
@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    username = request.json['username'].lower()
    password = request.json['password']
    if handler.credentials_valid(username, password):
        access_token = create_access_token(identity=username)
        tokens.append(access_token)
        user_data = handler.get_user_data(username)
        users.append(user_data)
        response = json.dumps({'access_token': access_token, 'user_data': user_data})
        return response
    return INVALID_CREDENTIALS

@app.route('/logout')
@cross_origin()
def logout():
    session['logged_in'] = False
    session['username'] = None
    return LOGIN

#============================SIGNUP=====================================
@app.route('/signup', methods=['POST'])
@cross_origin()
def signup():
    username = request.json['username'].lower()
    password = handler.hash_password(request.json['password'])
    email = request.json['email']
    invitation_code = request.json['invitationCode']
    if username == '' or password == '' or email == '':
        return EMPTY_ERROR
    if handler.username_exists(username) or len(username) < 8 or len(username) > 25:
        return USERNAME_ERROR
    elif handler.email_exists(email):
        return EMAIL_ERROR
    #elif len(password) < 8 or len(password) > 25: TODO just check in the front end lol, also this checks the hash not the actual password
        #return PASSWORD_ERROR
    else:
        handler.add_user(username, password, email) # TODO add invitation code here!!!
        # TODO add check to know if commit was successful===========================================
        access_token = create_access_token(identity=username)
        tokens.append(access_token)
        user_data = handler.get_user_data(username)
        users.append(user_data)
        response = {'access_token': access_token, 'user_data': user_data}
        return response
    return SIGNUP_ERROR

#==========================Settings=======================================
#@app.route('/settings', methods=['GET', 'POST'])
#def settings():
    #if session.get('logged_in'):
        #if request.method == 'POST':
            #old_password = request.json['old_password']
            #username = session['username']
            #new_password = request.json['new_password']
            #if handler.credentials_valid(username, old_password):
                #if new_password != '':
                    #password = handler.hash_password(new_password)
                    #handler.change_user(password=password)
                    #return json.dumps({'status': 'saved'})
                #return json.dumps({'status': 'Password empty'})
            #return json.dumps({'status': 'Wrong password'})
        #return flask.render_template('settings.html', user=handler.get_user())
    #return LOGIN
        

#=============================ERROR============================================
@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        return json.dumps({'error': str(e), 'code': e.code})
'''
@app.errorhandler(500)
'''