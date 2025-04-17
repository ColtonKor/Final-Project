import random
from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from PIL import Image
from datetime import datetime
import smtplib
from email.message import EmailMessage


# create an instance of Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap5(app)

# home page (about page)
@app.route('/')
def home():
    return render_template('home.html')

# steam page (lists games)
@app.route('/steam')
def steam():
    return render_template('steam.html')

# fortnite page (lists skins)
# maybe categorize between pickaxes or skins
@app.route('/fortnite')
def fortnite():
    return render_template('fornite.html')

@app.route('/login')
def login():
    return render_template('login.html')