import random
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from PIL import Image
from datetime import datetime
import bcrypt
import requests
from flask_mysqldb import MySQL
from flask_session import Session


# create an instance of Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap5(app)


@app.route('/steam')
def steam():
    return render_template('steam.html')

# fortnite page (lists skins)
# maybe categorize between pickaxes or skins
@app.route('/fortnite')
def fortnite():
    return render_template('fornite.html')


# Start of the Login Portion of the Code
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/createAccount')
def create_account():
    return render_template('signup.html')

@app.route('/welcome')
def welcome():
    if not session.get('authenticated'):
        return redirect('/')
    return render_template('home.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s', [username])
    user = cur.fetchone()
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        session['authenticated'] = True
        session['user'] = {
            'id': user['userId'],
            'username': user['username'],
            'firstName': user['firstName'],
            'lastName': user['lastName'],
            'pfp': user['profilePicture']
        }
        return render_template('welcome.html')
    return redirect('/')


@app.route('/signup', methods=['POST'])
def signup():
    fName = request.form['firstName']
    lName = request.form['lastName']
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s', [username])
    if cur.fetchone():
        return 'Username already taken.', 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    pfp_url = f'https://robohash.org/{username}.png?set=set4'

    cur.execute('INSERT INTO users (firstName, lastName, username, password, profilePicture) VALUES (%s, %s, %s, %s, %s)',
                (fName, lName, username, hashed, pfp_url))
    mysql.connection.commit()
    return render_template('login.html')

# End of the Login Portion of the Code