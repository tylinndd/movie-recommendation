# 🎬 Movie Recommendation System

My love and passion for film drove me to build a machine learning-based movie recommendation system that suggests movies based on a movie's genres, cast, description, and director. Built as part of a learning project to explore recommender systems and data science techniques, I plan to add more functionalities and features as my knowledge grows.
https://filmfanatic.onrender.com/

## 🧠 Technologies Used

- **Backend**: Python, Flask
- **Database**: SQLite, Flask-SQLAlchemy
- **Authentication**: Flask-Login, Flask-Bcrypt
- **Machine Learning**: Scikit-learn, Pandas
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Vercel/Render compatible

## 📌 Features

### Core Recommendation Engine
- Content-based filtering using movie metadata (genres, cast, directors, descriptions)
- Collaborative filtering (user/item-based)
- Hybrid recommendation model
- Interactive search with 10 personalized movie recommendations per query
- Visualizations of recommendation results

### User Authentication & Personal Features
- **Secure User Accounts**: Signup and login with encrypted passwords (bcrypt hashing)
- **Personal Watchlist**: Save movies you want to watch later
- **Already Watched List**: Track movies you've already seen with optional ratings
- **User Data Isolation**: Each user's lists are completely private and separate
- **Persistent Storage**: All data saved securely in SQLite database
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

## 🎯 How to Use

### Getting Started
1. Visit the app and create an account (username, email, password)
2. Log in to access all features
3. Start searching for movies!

### Search for Movies
1. Enter a movie title in the search bar
2. Click "Get Recommendations"
3. View the searched movie details and 10 personalized recommendations

### Manage Your Watchlist
1. Click the **green "Watchlist"** button on any movie card
2. Access your watchlist from the user menu (top-right corner)
3. Move movies to "Already Watched" or remove them

### Track Watched Movies
1. Click the **blue "Watched"** button on any movie card
2. Optionally add a rating for movies you've watched
3. View your complete watch history from the user menu

## 🔮 Future Enhancements

- Personal movie notes/reviews
- Movie statistics and insights dashboard
- Email verification and password reset functionality
- Share watchlists with friends
- Export watchlist/watched list (CSV, PDF)
- Advanced filtering and sorting options
- Movie rating system improvements
