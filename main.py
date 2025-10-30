from flask import Flask, request, jsonify, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Use PostgreSQL on Render, SQLite locally
database_url = os.environ.get('DATABASE_URL', 'sqlite:///movies.db')
# Fix for Render's postgres:// URL (SQLAlchemy needs postgresql://)
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure session cookies
# Use secure cookies only in production (Render uses HTTPS)
is_production = os.environ.get('DATABASE_URL') is not None
app.config['SESSION_COOKIE_SECURE'] = is_production  # Only send cookies over HTTPS in production
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['REMEMBER_COOKIE_SECURE'] = is_production
app.config['REMEMBER_COOKIE_HTTPONLY'] = True

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configure CORS to allow credentials (cookies)
# Since frontend and backend are served from the same Flask app (same-origin),
# CORS headers are added but same-origin requests will work automatically
CORS(app, supports_credentials=True)

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    watchlist = db.relationship('Watchlist', backref='user', lazy=True, cascade='all, delete-orphan')
    watched = db.relationship('WatchedList', backref='user', lazy=True, cascade='all, delete-orphan')

class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_title = db.Column(db.String(200), nullable=False)
    movie_data = db.Column(db.Text)  # Store JSON data about the movie
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

class WatchedList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_title = db.Column(db.String(200), nullable=False)
    movie_data = db.Column(db.Text)  # Store JSON data about the movie
    watched_at = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Float)  # Optional user rating

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Load and preprocess the dataset
df = pd.read_csv("movie_dataset.csv")
p_df = pd.read_csv("MovieGenre.csv", encoding='latin1')  # or try 'iso-8859-1' or 'cp1252'

features = ["keywords", "cast", "genres", "director"]
for feature in features:
    df[feature] = df[feature].fillna('')

def combine_features(row):
    return row['keywords'] + ' ' + row['cast'] + ' ' + row['genres'] + ' ' + row['director']

df["combined_features"] = df.apply(combine_features, axis=1)
count_matrix = CountVectorizer().fit_transform(df["combined_features"])
cosine_sim = cosine_similarity(count_matrix)

def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]

def get_movie_details(index):
    movie = df[df.index == index].iloc[0]
    # Use TMDB API poster path if available, otherwise use placeholder
    # For now, we'll use OMDB API style poster with IMDB ID or create a nice placeholder
    tmdb_id = int(movie["id"]) if pd.notna(movie["id"]) else None
    
    # Try constructing poster URL - TMDB uses poster_path which we need to fetch separately
    # For now, using a reliable poster service that works with TMDB IDs
    poster_url = f"https://image.tmdb.org/t/p/w500//{tmdb_id}.jpg" if tmdb_id else None
    
    return {
        "title": movie["title"],
        "overview": movie["overview"] if pd.notna(movie["overview"]) else "No description available.",
        "tagline": movie["tagline"] if pd.notna(movie["tagline"]) else "",
        "release_date": movie["release_date"] if pd.notna(movie["release_date"]) else "Unknown",
        "vote_average": float(movie["vote_average"]) if pd.notna(movie["vote_average"]) else 0,
        "runtime": int(movie["runtime"]) if pd.notna(movie["runtime"]) else 0,
        "genres": movie["genres"] if pd.notna(movie["genres"]) else "",
        "poster_url": poster_url,
        "tmdb_id": tmdb_id,
        "use_placeholder": True  # Flag to indicate we should use styled placeholder
    }

def get_index_from_title(title):
    try:
        return df[df.title == title]["index"].values[0]
    except:
        return None

# Authentication Routes
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return jsonify({
        'message': 'User created successfully',
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email
        }
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200
    
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/current_user', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email
            }
        }), 200
    return jsonify({'authenticated': False}), 200

# Watchlist Routes
@app.route('/api/watchlist', methods=['GET'])
@login_required
def get_watchlist():
    watchlist_items = Watchlist.query.filter_by(user_id=current_user.id).order_by(Watchlist.added_at.desc()).all()
    import json
    return jsonify([{
        'id': item.id,
        'movie_title': item.movie_title,
        'movie_data': json.loads(item.movie_data) if item.movie_data else None,
        'added_at': item.added_at.isoformat()
    } for item in watchlist_items]), 200

@app.route('/api/watchlist', methods=['POST'])
@login_required
def add_to_watchlist():
    data = request.get_json()
    movie_title = data.get('movie_title')
    movie_data = data.get('movie_data')

    if not movie_title:
        return jsonify({'error': 'Movie title is required'}), 400

    # Check if already in watchlist
    existing = Watchlist.query.filter_by(user_id=current_user.id, movie_title=movie_title).first()
    if existing:
        return jsonify({'error': 'Movie already in watchlist'}), 400

    import json
    new_item = Watchlist(
        user_id=current_user.id,
        movie_title=movie_title,
        movie_data=json.dumps(movie_data) if movie_data else None
    )
    
    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        'message': 'Added to watchlist',
        'id': new_item.id
    }), 201

@app.route('/api/watchlist/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_watchlist(item_id):
    item = Watchlist.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Removed from watchlist'}), 200

# Watched List Routes
@app.route('/api/watched', methods=['GET'])
@login_required
def get_watched():
    watched_items = WatchedList.query.filter_by(user_id=current_user.id).order_by(WatchedList.watched_at.desc()).all()
    import json
    return jsonify([{
        'id': item.id,
        'movie_title': item.movie_title,
        'movie_data': json.loads(item.movie_data) if item.movie_data else None,
        'watched_at': item.watched_at.isoformat(),
        'rating': item.rating
    } for item in watched_items]), 200

@app.route('/api/watched', methods=['POST'])
@login_required
def add_to_watched():
    data = request.get_json()
    movie_title = data.get('movie_title')
    movie_data = data.get('movie_data')
    rating = data.get('rating')

    if not movie_title:
        return jsonify({'error': 'Movie title is required'}), 400

    # Check if already in watched list
    existing = WatchedList.query.filter_by(user_id=current_user.id, movie_title=movie_title).first()
    if existing:
        return jsonify({'error': 'Movie already in watched list'}), 400

    # Remove from watchlist if it exists there
    watchlist_item = Watchlist.query.filter_by(user_id=current_user.id, movie_title=movie_title).first()
    if watchlist_item:
        db.session.delete(watchlist_item)

    import json
    new_item = WatchedList(
        user_id=current_user.id,
        movie_title=movie_title,
        movie_data=json.dumps(movie_data) if movie_data else None,
        rating=rating
    )
    
    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        'message': 'Added to watched list',
        'id': new_item.id
    }), 201

@app.route('/api/watched/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_watched(item_id):
    item = WatchedList.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Removed from watched list'}), 200

@app.route('/api/check_movie_status/<title>', methods=['GET'])
@login_required
def check_movie_status(title):
    in_watchlist = Watchlist.query.filter_by(user_id=current_user.id, movie_title=title).first() is not None
    in_watched = WatchedList.query.filter_by(user_id=current_user.id, movie_title=title).first() is not None
    return jsonify({
        'in_watchlist': in_watchlist,
        'in_watched': in_watched
    }), 200

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    movie_title = request.args.get('title')
    movie_index = get_index_from_title(movie_title)
    if movie_index is None:
        return jsonify({"error": "Movie not found", "searched_movie": None, "recommendations": []})

    # Get details of the searched movie
    searched_movie = get_movie_details(movie_index)
    
    # Get similar movies
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:11]
    recommendations = [get_movie_details(movie[0]) for movie in sorted_movies]
    
    return jsonify({
        "searched_movie": searched_movie,
        "recommendations": recommendations
    })

@app.route('/movie/<title>', methods=['GET'])
def get_movie(title):
    movie_index = get_index_from_title(title)
    if movie_index is None:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify(get_movie_details(movie_index))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

