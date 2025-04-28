from flask import Flask, render_template, request, redirect, session, jsonify
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from PIL import Image
from datetime import datetime
import bcrypt
import requests
from flask_sqlalchemy import SQLAlchemy


# create an instance of Flask
db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres.bkvgncwmwqudmgkhngiu:ColtonDatabasePassword1@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
db.init_app(app)


app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap5(app)


@app.route('/steam')
def steam():
    if not session.get('authenticated'):
        return redirect('/')
    return render_template('steam.html')

# fortnite page (lists skins)
# maybe categorize between pickaxes or skins
@app.route('/fortnite')
def fortnite():
    if not session.get('authenticated'):
        return redirect('/')

    user = session.get('user')
    pfp = user.get('pfp')
    
    cosmetics = fetch_cosmetic(None, None, None)
    return render_template('fortnite.html', list=cosmetics, pfp=pfp)


@app.route('/sortFortnite', methods=['POST'])
def sortFortnite():
    if not session.get('authenticated'):
        return redirect('/')
    
    user = session.get('user')
    pfp = user.get('pfp')
    username = user.get('username')

    type = request.form['type']
    rarity = request.form['rarity']
    search = request.form['search']
    cosmetics = fetch_cosmetic(type, rarity, search)
    return render_template('fortnite.html', list=cosmetics, pfp=pfp, username=username)


@app.route('/addFavorite', methods=['POST'])
def favoriteCosmetic():
    image = request.form['image']
    name = request.form['name']
    description = request.form['description']
    introduction = request.form['introduction']
    type = request.form['type']
    rarity = request.form['rarity']
    series = request.form['series']
    set = request.form['set']

    new_favorite = Favorite(
        user_id=session['user']['id'],
        skinname=name,
        description=description,
        series=series,
        rarity=rarity,
        set=set,
        type=type,
        image=image,
        introduced=introduction
    )

    db.session.add(new_favorite)
    db.session.commit()

    return redirect('/fortnite')


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

@app.route('/account', methods=['GET', 'POST'])
def account():
    is_fortnite = True

    if request.method == 'POST':
        t = request.form.get('type')
        if t == 'fortnite':
            is_fortnite = True
        else:
            is_fortnite = False

    user = session.get('user')
    favorites = Favorite.query.filter_by(user_id=user.get('id')).all()
    
    return render_template('account.html', user=user, favorites=favorites, is_fortnite=is_fortnite)
@app.route('/welcome')
def welcome():
    if not session.get('authenticated'):
        return redirect('/')
    return render_template('home.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        
        session['authenticated'] = True
        session['user'] = {
            'id': user.user_id,
            'username': user.username,
            'firstName': user.firstname,
            'lastName': user.lastname,
            'pfp': user.profilepicture
        }
        return render_template('home.html')
    return redirect('/')


@app.route('/signup', methods=['POST'])
def signup():
    fName = request.form['firstName']
    lName = request.form['lastName']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    if User.query.filter_by(username=username).first():
        return 'Username already taken.', 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    pfp_url = f'https://robohash.org/{username}.png?set=set4'

    new_user = User(
        firstname=fName,
        lastname=lName,
        username=username,
        password=hashed,
        profilepicture=pfp_url,
        email=email
    )
    db.session.add(new_user)
    db.session.commit()

    return render_template('login.html')



class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profilepicture = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True, nullable=False)


class Favorite(db.Model):
    __tablename__ = 'favorite'
    skin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    skinname = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    series = db.Column(db.String(80), nullable=False)
    rarity = db.Column(db.String(255), nullable=False)
    set = db.Column(db.String(255))
    type = db.Column(db.String(255))
    image = db.Column(db.String(120), unique=True, nullable=False)
    introduced = db.Column(db.String(120), nullable=False)


def fetch_cosmetic(type, rarity, search):
    r = requests.get('https://fortnite-api.com/v2/cosmetics/br')
    all_cosmetics = r.json().get("data", [])
    filtered_cosmetics = all_cosmetics
    if type:
        filtered_cosmetics = [item for item in filtered_cosmetics if item.get("type", {}).get("value") == type]
    if rarity:
        filtered_cosmetics = [item for item in filtered_cosmetics if item.get("rarity", {}).get("backendValue") == "EFortRarity::"+rarity]
    if search:
        filtered_cosmetics = [item for item in filtered_cosmetics if search.lower() in item.get("name", "").lower()]
    return filtered_cosmetics
# End of the Login Portion of the Code