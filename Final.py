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
from flask_mail import Mail, Message
import time


# create an instance of Flask
db = SQLAlchemy()
app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'MultimediaFinalProject12@gmail.com'  # Use environment variables in production
app.config['MAIL_PASSWORD'] = 'halz raws xxjf wxmb'

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres.bkvgncwmwqudmgkhngiu:ColtonDatabasePassword1@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
db.init_app(app)


app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap5(app)
mail = Mail(app)


@app.route('/steam')
def steam():
    if not session.get('authenticated'):
        return redirect('/')

    user = session.get('user')
    pfp = user.get('pfp')

    page = int(request.args.get('page', 1))
    per_page = 54

    deals = fetch_free_games(None, None, None, None)

    start = (page - 1) * per_page
    end = start + per_page
    paginated_games = deals[start:end]

    has_next = len(deals) > end
    has_prev = page > 1

    genres = sorted(set(game['genre'] for game in deals))
    platforms = sorted(set(game['platform'] for game in deals))
    publishers = sorted(set(game['publisher'] for game in deals))

    return render_template('steam.html', games=paginated_games, pfp=pfp, genres=genres, platforms=platforms, publishers=publishers, page=page, has_next=has_next, has_prev=has_prev)

#use the fetch_game_title(query) 
@app.route('/sortSteam', methods=['GET', 'POST'])
def sortSteam():
    if not session.get('authenticated'):
        return redirect('/')

    user = session.get('user')
    pfp = user.get('pfp')

    if request.method == 'POST':
        genre = request.form['genre']
        publisher = request.form['publisher']
        platform = request.form['platform']
        search = request.form['search']
    else:
        genre = request.args.get('genre', '')
        publisher = request.args.get('publisher', '')
        platform = request.args.get('platform', '')
        search = request.args.get('search', '')

    page = int(request.args.get('page', 1))
    per_page = 54

    deals = fetch_free_games(genre, publisher, platform, search)

    start = (page - 1) * per_page
    end = start + per_page
    paginated_games = deals[start:end]

    has_next = len(deals) > end
    has_prev = page > 1


    regular = fetch_free_games(None, None, None, None)

    genres = sorted(set(game['genre'] for game in regular))
    platforms = sorted(set(game['platform'] for game in regular))
    publishers = sorted(set(game['publisher'] for game in regular))

    return render_template('steam.html', games=paginated_games, pfp=pfp, genres=genres, platforms=platforms, publishers=publishers, page=page, has_next=has_next, has_prev=has_prev)


@app.route('/addSteam', methods=['POST'])
def favoriteGame():
    title = request.form['title']
    thumbnail = request.form['thumb']
    genre = request.form['genre']
    short_description = request.form['description']
    platform = request.form['platform']
    publisher = request.form['publisher']
    developer = request.form['developer']
    release_date = request.form['release']
    url = request.form.get('url')

    new_favorite = Free(
        user_id=session['user']['id'],
        title=title,
        thumbnail=thumbnail,
        genre=genre,
        short_description=short_description,
        platform=platform,
        publisher=publisher,
        developer=developer,
        release_date=release_date,
        url=url
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({'success': True})


@app.route('/removeSteam', methods=['POST'])
def deleteGame():
    id = request.form['id']
    favorite = Free.query.filter_by(game_id=id).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()

    return redirect(f'/account?currentTab={2}')

# fortnite page (lists skins)
# maybe categorize between pickaxes or skins
@app.route('/fortnite')
def fortnite():
    if not session.get('authenticated'):
        return redirect('/')

    user = session.get('user')
    pfp = user.get('pfp')

    page = int(request.args.get('page', 1))
    per_page = 54

    all_cosmetics = fetch_cosmetic(None, None, None)

    #pages
    start = (page - 1) * per_page
    end = start + per_page
    paginated_cosmetics = all_cosmetics[start:end]

    has_next = len(all_cosmetics) > end
    has_prev = page > 1
    
    return render_template('fortnite.html', list=paginated_cosmetics, page=page, has_next=has_next, has_prev=has_prev, pfp=pfp)


@app.route('/sortFortnite', methods=['GET', 'POST'])
def sortFortnite():
    if not session.get('authenticated'):
        return redirect('/')
    
    user = session.get('user')
    pfp = user.get('pfp')

    if request.method == 'POST':
        type = request.form['type']
        rarity = request.form['rarity']
        search = request.form['search']
    else:
        type = request.args.get('type', '')
        rarity = request.args.get('rarity', '')
        search = request.args.get('search', '')
    
    cosmetics = fetch_cosmetic(type, rarity, search)
    #pages
    page = int(request.args.get('page', 1))
    per_page = 54

    start = (page - 1) * per_page
    end = start + per_page
    paginated_cosmetics = cosmetics[start:end]

    has_next = len(cosmetics) > end
    has_prev = page > 1

    return render_template('fortnite.html', list=paginated_cosmetics, page=page, has_next=has_next, has_prev=has_prev, pfp=pfp, type=type, rarity=rarity, search=search)


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

    return jsonify({'success': True})


@app.route('/removeFavorite', methods=['POST'])
def deleteCosmetic():
    id = request.form['id']
    favorite = Favorite.query.filter_by(skin_id=id).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()

    return redirect(f'/account?currentTab={1}')


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

@app.route('/account')
def account():
    current_tab = request.args.get('currentTab')
    is_fortnite = (current_tab == '1')

    user = session.get('user')
    favoriteCosmetics = Favorite.query.filter_by(user_id=user.get('id')).all()
    favoriteGames = Free.query.filter_by(user_id=user.get('id')).all()
    
    return render_template('account.html', user=user, favoriteCosmetics=favoriteCosmetics, favoriteGames=favoriteGames, is_fortnite=is_fortnite)

@app.route('/emailUser', methods=['POST'])
def emailAvailability():
    email_body = f""

    user = session.get('user')
    favoriteCosmetics = Favorite.query.filter_by(user_id=user.get('id')).all()
    currentShop = fetch_fortnite_shop()
    notified_items = set()

    #Hello is this here?
    for item in favoriteCosmetics:
        for entry in currentShop['entries']:
            for br_item in entry.get('brItems', []):
                if item.skinname.lower() == br_item['name'].lower():
                    if item.skinname.lower() not in notified_items:
                        email_body += f"Your favorited item: {item.skinname} is currently in the shop.\n"
                        notified_items.add(item.skinname.lower())

    msg = Message(
        subject='One or more favorited items are in the Shop!',
        sender=app.config['MAIL_USERNAME'],
        recipients=[session['user']['email']],
        body=email_body
    )

    if(email_body):
        mail.send(msg)
   
    return redirect(f'/account?currentTab={1}')


@app.route('/welcome')
def welcome():
    if not session.get('authenticated'):
        return redirect('/')
    
    return render_template('home.html')

@app.route('/delete')
def deleteAccount():
    account = User.query.filter_by(user_id=session['user']['id']).first()

    if account:
        db.session.delete(account)
        db.session.commit()

    session.clear()
    return render_template('login.html')

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
            'email' : user.email,
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

class Steam(db.Model):
    __tablename__ = 'steam'
    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    image = db.Column(db.String(120), unique=True, nullable=False)
    gamename = db.Column(db.String(100), nullable=False)
    saleprice = db.Column(db.String(100), nullable=False)
    regularprice = db.Column(db.String(80), nullable=False)
    deal_id = db.Column(db.String(255), nullable=False)
    steam_id = db.Column(db.String(255), nullable=False)

class Free(db.Model):
    __tablename__ = 'free'
    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    thumbnail = db.Column(db.String(256), nullable=False)
    genre = db.Column(db.String(64), nullable=True)
    short_description = db.Column(db.String(256), nullable=True)
    platform = db.Column(db.String(64), nullable=True)
    publisher = db.Column(db.String(128), nullable=True)
    developer = db.Column(db.String(128), nullable=True)
    release_date = db.Column(db.String(256), nullable=True)
    url = db.Column(db.String(256), nullable=True)


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

    # if(filtered_cosmetics == all_cosmetics):
        
    return filtered_cosmetics


def fetch_fortnite_shop():
    r = requests.get('https://fortnite-api.com/v2/shop')
    all_cosmetics = r.json().get("data", [])
    return all_cosmetics

def fetch_free_games(genre, publisher, platform, search):
    r = requests.get('https://www.freetogame.com/api/games')
    all_games = r.json()

    filtered_games = all_games

    if genre:
        genre = genre.lower().strip()
        filtered_games = [
            game for game in filtered_games
            if genre in normalize_genre(game.get('genre', ''))
        ]

    if publisher:
        publisher = publisher.lower()
        filtered_games = [
            game for game in filtered_games
            if publisher in game.get('publisher', '').lower()
        ]

    if platform:
        platform = platform.lower()
        filtered_games = [
            game for game in filtered_games
            if platform in game.get('platform', '').lower()
        ]

    if search:
        search = search.lower()
        filtered_games = [
            game for game in filtered_games
            if search in game.get('title', '').lower()
            or search in game.get('short_description', '').lower()
        ]

    return filtered_games

# Steam Store Games
def fetch_game_title(query):
    r = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    games = r.json()["applist"]["apps"]

    for game in games:
        if query.lower() in game["name"].lower():
            return game["appid"], game["name"]
    return None, None

def fetch_steamid_deal(steamID):
    r = requests.get(f'https://www.cheapshark.com/api/1.0/games?steamAppID={steamID}')

    return r.json()

def search_game(query):
    steam_id, title = fetch_game_title(query)
    if not steam_id:
        return f"No Steam game found for: {query}"

    print(f"Found '{title}' on Steam (appid: {steam_id})")

    deal_info = fetch_steamid_deal(steam_id)
    if deal_info:
        return deal_info #thumbnail, title, steamid, original price, sale price
    else:
        return f"No CheapShark deal found for: {title}"

def fetch_sale_games():
    r = requests.get("https://www.cheapshark.com/api/1.0/deals", params={
        "storeID": "1",
        "pageSize": 5,
        "sortBy": "recent"
    })

    return r.json()



def normalize_genre(genre_str):
    # Normalize genres to lowercase and split by common separators
    return [g.strip().lower() for g in genre_str.replace('/', ',').replace('|', ',').split(',') if g.strip()]