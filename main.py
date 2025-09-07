from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load and preprocess the dataset
df = pd.read_csv("movie_dataset.csv")
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
        return jsonify([])

    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:11]
    recommendations = [get_title_from_index(movie[0]) for movie in sorted_movies]
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)

