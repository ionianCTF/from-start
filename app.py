#!/user/bin/env python3
from scripts import database, handler
import flask
from werkzeug.exceptions import HTTPException
import json
import sys
import os

app = flask.Flask(__name__)
app.config["CACHE_TYPE"] = 'null'
app.secret_key = os.urandom(12)
#testing
app.config["TEMPLATES_AUTO_RELOAD"]= True

# Messages to return

HOMEPAGE = json.dumps({'render': 'home'})
WELCOME = json.dumps({'render': 'WELCOME'})
LOGIN = json.dumps({'render': 'login'})
SIGNUP = json.dumps({'render': 'signup'})
SUCCESS = json.dumps({'success': False})
FAILURE = json.dumps({'success': False})
USERNAME_ERROR = json.dumps({'status': 'username_unavailable'})
EMAIL_ERROR = json.dumps({'status': 'email_unavailable'})
PASSWORD_ERROR = json.dumps({'status': 'password_error'})
EMPTY_ERROR = json.dumps({'status': 'empty_fields'})

#==============================WELCOME-PAGE================================
@app.route('/', methods=['GET', 'POST'])
def WELCOME():
    if flask.session.get('logged_in'):
        return HOMEPAGE    
    return WELCOME

#==============================LOGIN===================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if not flask.session.get('logged_in'):
        if flask.request.method == 'POST':
            username = flask.request.form['username'].lower()
            password = flask.request.form['password']
            if handler.credentials_valid(username, password):
                flask.session['logged_in'] = True
                flask.session['username'] = username
                return SUCCESS
            return FAILURE
        return LOGIN
    return HOMEPAGE

@app.route("/logout")
def logout():
    flask.session['logged_in'] = False
    flask.session['username'] = None
    return LOGIN

#============================SIGNUP=====================================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not flask.session.get('logged_in'):
        if flask.request.method == 'POST':
            print(flask.request.data)
            username = flask.request.form['username'].lower()
            password = handler.hash_password(flask.request.form['password'])
            email = flask.request.form['email']
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
                flask.session['logged_in'] = True
                flask.session['username'] = username
                # TODO add check to know if commit was successful===========================================
                return SUCCESS
        return SIGNUP
    return HOMEPAGE

#==========================Settings=======================================
#@app.route('/settings', methods=['GET', 'POST'])
#def settings():
    #if flask.session.get('logged_in'):
        #if flask.request.method == 'POST':
            #old_password = flask.request.form['old_password']
            #username = flask.session['username']
            #new_password = flask.request.form['new_password']
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