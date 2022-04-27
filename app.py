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

# Objects to return
render = {
    homepage: json.dumps({'render': 'home'}),
    welcome: json.dumps({'render': 'welcome'}),
    login: json.dumps({'render': 'login'}),
    signup: json.dumps({'render': 'signup'})
}
success = json.dumps({'success': False})
failure = json.dumps({'success': False})
signup_error = {
    username: json.dumps({'status': 'username_unavailable'}),
    email: json.dumps({'status': 'email_unavailable'}),
    passwords: json.dumps({'status': 'password_error'}),
    empty: json.dumps({'status': 'empty_fields'})
}

#==============================WELCOME-PAGE================================
@app.route('/', methods=['GET', 'POST'])
def welcome():
    if flask.session.get('logged_in'):
        return render.homepage    
    return render.welcome

#==============================login===================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if not flask.session.get('logged_in'):
        if flask.request.method == 'POST':
            username = flask.request.form['username'].lower()
            password = flask.request.form['password']
            if handler.credentials_valid(username, password):
                flask.session['logged_in'] = True
                flask.session['username'] = username
                return success
            return failure
        return render.login
    return render.homepage

@app.route("/logout")
def logout():
    flask.session['logged_in'] = False
    flask.session['username'] = None
    return render.login

#============================SIGNUP=====================================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not flask.session.get('logged_in'):
        if flask.request.method == 'POST':
            username = flask.request.form['username'].lower()
            password = handler.hash_password(flask.request.form['password'])
            email = flask.request.form['email']
            if username != '' or password != '' or conf_password != '':
                return signup_error.empty
            if handler.username_exists(username) or len(username) < 8 or len(username) > 25:
                return signup_error.username
            elif handler.email_exists(email):
                return signup_error.email
            elif len(password) < 8 or len(password) > 25:
                return signup_error.password
            else:
                handler.add_user(username, password, email)
                flask.session['logged_in'] = True
                flask.session['username'] = username
                # TODO add check to know if commit was successful===========================================
                return success
        return render.signup
    return render.homepage

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
    #return render.login
        

#=============================ERROR============================================
@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        return json.dumps({'error': str(e), 'code': e.code})
'''
@app.errorhandler(500)
'''