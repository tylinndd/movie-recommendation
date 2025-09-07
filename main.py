import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#read the csv file
df = pd.read_csv("/Users/tylin/movie-recommendation/movie_dataset.csv")
print(df.columns)

def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]

##Step 2: Select Features
features = ["keywords","case","genres","director"]
for feature in features:
    df[feature] = df[feature].fillna('')
##Step 3: Create a column in DF which combines all selected features
all_features = df["keywords"] + ' ' + df["case"] + ' ' + df["genres"] + ' ' + df["director"]
df["all_features"] = all_features
##Step 4: Create count matrix from this new combined column
count_matrix = CountVectorizer().fit_transform(df["all_features"])
##Step 5: Compute the Cosine Similarity based on the count_matrix
cosine_similarity = cosine_similarity(count_matrix)
movie_user_likes = "Avatar"

## Step 6: Get index of this movie from its title

## Step 7: Get a list of similar movies in descending order of similarity score


## Step 8: Print titles of first 50 movies

 