# 🎬 Movie Recommendation System

My love and passion for film drove me to build a machine learning-based movie recommendation system that suggests movies based on a movie's genres, cast, description, and director. Built as part of a learning project to explore recommender systems and data science techniques, I plan to add more functionalities and features as my knowledge grows.

## 📌 Features

### Core Recommendation Features
- Content-based filtering  
- Collaborative filtering (user/item-based)  
- Hybrid recommendation model  
- Movie metadata analysis (genres, cast, directors, etc.)  
- Interactive user interface  
- Visualizations of recommendation results  

### 🔐 NEW: User Authentication & Personal Features
- **User Accounts**: Secure signup and login with encrypted passwords
- **Personal Watchlist**: Save movies you want to watch later
- **Already Watched List**: Track movies you've already seen
- **User Data Isolation**: Each user's lists are completely private and separate
- **Persistent Storage**: All your data is saved in a secure database
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

## 🧠 Technologies Used

- Python
- Flask  
- Flask-SQLAlchemy (Database ORM)
- Flask-Login (User session management)
- Flask-Bcrypt (Password encryption)
- Pandas
- HTML/CSS/JavaScript
- Scikit-learn
- SQLite Database
- Bash

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd movie-recommendation
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

**Note:** If you encounter SSL certificate errors, see `SETUP_GUIDE.md` for solutions.

3. **Run the application**
```bash
python main.py
```

4. **Open in browser**
```
http://localhost:5000
```

### First Time Use

1. You'll see a login page when you first visit
2. Click **"Sign up"** to create your account
3. Enter a unique username, email, and password (minimum 6 characters)
4. You'll be automatically logged in and can start using the app!

## 📖 Documentation

- **[AUTH_FEATURES.md](AUTH_FEATURES.md)** - Complete guide to authentication and user features
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup instructions and troubleshooting
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deploy your app to production

## 🎯 How to Use

### Search for Movies
1. Enter a movie title in the search bar
2. Click "Get Recommendations"
3. View the searched movie details and 10 personalized recommendations

### Manage Your Watchlist
1. Click the **green "Watchlist"** button on any movie
2. Access your watchlist from the user menu (top-right corner)
3. Move movies to "Already Watched" or remove them

### Track Watched Movies
1. Click the **blue "Watched"** button on any movie
2. View your watched history from the user menu
3. Keep track of all the movies you've seen!

## 🔒 Security Features

- ✅ Passwords encrypted with bcrypt hashing
- ✅ Secure session management
- ✅ User data isolation (you can only see your own data)
- ✅ Protected API endpoints
- ✅ SQLite database with proper access controls

## 🧪 Testing

Run the authentication test script:
```bash
python test_auth.py
```

This will verify:
- All packages are installed correctly
- Database is working
- User creation and authentication work
- Watchlist and watched list features function properly

## 📁 Project Structure

```
movie-recommendation/
├── main.py                 # Flask app with authentication
├── index.html             # Main UI with login/signup
├── static/
│   ├── style.css          # Styling for all features
│   └── app.js             # Frontend authentication logic
├── movie_dataset.csv      # Movie data
├── MovieGenre.csv         # Genre data
├── movies.db              # SQLite database (auto-created)
├── requirements.txt       # Python dependencies
├── test_auth.py          # Authentication test script
├── AUTH_FEATURES.md      # Feature documentation
├── SETUP_GUIDE.md        # Setup instructions
└── DEPLOYMENT_GUIDE.md   # Deployment guide
```

## 🐛 Troubleshooting

**Can't install packages?**
- See `SETUP_GUIDE.md` for SSL certificate solutions

**Login not working?**
- Clear browser cookies
- Try creating a new account
- Check browser console for errors

**Movies not saving to lists?**
- Make sure you're logged in (username visible in top-right)
- Refresh the page and try again

## 🔮 Future Enhancements

- User ratings for watched movies
- Personal movie notes/reviews
- Movie statistics and insights
- Email verification
- Password reset functionality
- Share watchlists with friends
- Export watchlist/watched list
- Advanced filtering and sorting

## 📝 Version History

**v2.0** - Added user authentication and personal features
- User signup/login/logout
- Personal watchlist
- Already watched list
- Secure database storage
- Complete UI overhaul

**v1.0** - Initial release
- Movie recommendations
- Content-based filtering
- Basic UI
