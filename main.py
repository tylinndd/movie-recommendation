import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv("/Users/tylin/movie-recommendation/movie_dataset.csv")


def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]


features = ["keywords","cast","genres","director"]
for feature in features:
    df[feature] = df[feature].fillna('')
def combine_features(row):
    try:
        return row['keywords'] + ' ' + row['cast'] + ' ' + row['genres'] + ' ' + row['director']
    except:
        print("Error:", row)

df["combined_features"] = df.apply(combine_features, axis=1)
print(df["combined_features"].head())      



count_matrix = CountVectorizer().fit_transform(df["combined_features"])

cosine_similarity = cosine_similarity(count_matrix)
movie_user_likes = "Avatar"
movie = get_index_from_title(movie_user_likes)
similar_movies = list(enumerate(cosine_similarity[movie]))
similar_movies_sorted = sorted(similar_movies, key= lambda x:x[1],reverse = True)
i=0
for movie in similar_movies_sorted:
    print(get_title_from_index(movie[0]))
    i=i+1
    if i>50:
        break

 