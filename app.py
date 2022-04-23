#!/user/bin/env python3
from scripts import database, forms, handler
from flask import Flask, redirect, url_for, render_template, request, session
import json
import sys
import os
import ast

app = Flask(__name__)
app.config["CACHE_TYPE"] = 'null'
app.secret_key = os.urandom(12)


#==============================LOGIN===================================
@app.route('/', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            print(username, password)
            if form.validate():
                if handler.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/passw'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html')
    user = handler.get_user()
    return render_template('home.html', user=user)




#============================SIGNUP=====================================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = handler.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if not handler.username_taken(username):
                    handler.add_user(username, password, email)
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Signup successful'})
                return json.dumps({'status': 'User/Pass required'})
            return render_template('login.html', form=form)
        return render_template('signup.html')
    return render_template('home.html', user=user)
