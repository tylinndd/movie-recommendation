from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

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
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

