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

#==============================HOMEPAGE================================
@app.route('/', methods=['GET', 'POST'])
def welcome():
    if flask.session.get('logged_in'):
        return flask.render_template('home.html', user=handler.get_user())
    return flask.render_template('welcome.html')

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
                return json.dumps({'success': True})
            return json.dumps({'success': False})
        return flask.render_template('login.html')
    return flask.render_template('home.html', user=handler.get_user())

@app.route("/logout")
def logout():
    flask.session['logged_in'] = False
    flask.session['username'] = None
    return flask.redirect(flask.url_for('login'))

#============================SIGNUP=====================================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not flask.session.get('logged_in'):
        if flask.request.method == 'POST':
            username = flask.request.form['username'].lower()
            password = handler.hash_password(flask.request.form['password'])
            conf_password = handler.hash_password(flask.request.form['confirm-pass'])
            email = flask.request.form['email']
            if username != '' and password != '' and conf_password != '':
                if handler.username_available(username):
                    return json.dumps({'status': 'username_unavailable'})
                elif handler.email_available(email):
                    return json.dumps({'status': 'email_unavailable'})
                elif password != conf_password:
                    return json.dumps({'status': 'not_match'})
                else:
                    handler.add_user(username, password, email)
                    flask.session['logged_in'] = True
                    flask.session['username'] = username
                    return flask.render_template('home.html', user=handler.get_user())
            return json.dumps({'status': 'empty_fields'})
        return flask.render_template('signup.html')
    return flask.render_template('home.html', user=handler.get_user())

#==========================Settings=======================================
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if flask.session.get('logged_in'):
        if flask.request.method == 'POST':
            old_password = flask.request.form['old_password']
            username = flask.session['username']
            new_password = flask.request.form['new_password']
            if handler.credentials_valid(username, old_password):
                if new_password != "":
                    password = handler.hash_password(new_password)
                    handler.change_user(password=password)
                    return json.dumps({'status': 'saved'})
                return json.dumps({'status': 'Password empty'})
            return json.dumps({'status': 'Wrong password'})
        return flask.render_template('settings.html', user=handler.get_user())
    return flask.redirect(flask.url_for('login'))
        

#=========+++=================ERROR============================================
@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return json.dumps({'error': str(e), 'code': code})