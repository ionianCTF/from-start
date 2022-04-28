#!/user/bin/env python3
from scripts import database, handler
from flask import Flask, session, request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from werkzeug.exceptions import HTTPException
from datetime import timedelta
import json
import sys
import os

app = Flask(__name__)
#============================TOKEN-CONFIG==================================
app.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)
access_token = None

# Token refresh timer
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

#=============================RESPONSES====================================
HOMEPAGE = json.dumps({'render': 'home'})
WELCOME = json.dumps({'render': 'welcome'})
LOGIN = json.dumps({'render': 'login'})
SIGNUP = json.dumps({'render': 'signup'})
SUCCESS = json.dumps({'success': True})
FAILURE = json.dumps({'success': False})
USERNAME_ERROR = json.dumps({'status': 'username_unavailable'})
EMAIL_ERROR = json.dumps({'status': 'email_unavailable'})
PASSWORD_ERROR = json.dumps({'status': 'password_error'})
EMPTY_ERROR = json.dumps({'status': 'empty_fields'})

TEST_RESPONSE = json.dumps({'test': 'test_response'})


#==============================WELCOME-PAGE================================
@app.route('/', methods=['GET', 'POST'])
def welcome():
    if access_token is not None:
        return HOMEPAGE
    return WELCOME

#==============================LOGIN===================================
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username'].lower()
    password = request.json['password']
    if handler.credentials_valid(username, password):
        access_token = create_access_token(identity=username)
        response = {"access_token": access_token}
        return response
    return FAILURE

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = None
    return LOGIN

#============================SIGNUP=====================================
@app.route('/signup', methods=['POST'])
def signup():
    username = request.json['username'].lower()
    password = handler.hash_password(request.json['password'])
    email = request.json['email']
    if username != '' or password != '' or conf_password != '':
        return EMPTY_ERROR
    if handler.username_exists(username) or len(username) < 8 or len(username) > 25:
        return USERNAME_ERROR
    elif handler.email_exists(email):
        return EMAIL_ERROR
    elif len(password) < 8 or len(password) > 25:
        return PASSWORD_ERROR
    else:
        handler.add_user(username, password, email)
        session['logged_in'] = True
        session['username'] = username
        # TODO add check to know if commit was successful===========================================
        return SUCCESS

#==========================Settings=======================================
#@app.route('/settings', methods=['GET', 'POST'])
#def settings():
    #if session.get('logged_in'):
        #if request.method == 'POST':
            #old_password = request.json['old_password']
            #username = session['username']
            #new_password = request.json['new_password']
            #if handler.credentials_valid(username, old_password):
                #if new_password != "":
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