import sys
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(model_url)
print('Model Loaded')

def embed(texts):
    return model(texts)

df = pd.read_csv("/home/pc/Desktop/Begining/webdev/HackOn/Final/Backend/LLM/1.csv", engine="python")
df = df[["id", "overview", "popularity", "original_title", "original_language"]]
df = df.dropna()
df = df.reset_index()
df = df[:5500]

df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce')

non_numeric_rows = df[df['popularity'].isna()]
if not non_numeric_rows.empty:
    print("Warning: Some rows in the 'popularity' column contain non-numeric values and have been set to NaN.")
    print(non_numeric_rows)

titles = list(df['overview'])
embeddings = embed(titles)

nn = NearestNeighbors(n_neighbors=50)
nn.fit(embeddings)

def recommend(movie1_id, movie2_id, selected_languages):
    movie1_row = df[df['id'] == movie1_id]
    movie2_row = df[df['id'] == movie2_id]

    if movie1_row.empty or movie2_row.empty:
        print('Invalid movie id(s).')
        return

    movie1, movie1_languages = movie1_row.iloc[0]['overview'], movie1_row.iloc[0]['original_language']
    movie2, movie2_languages = movie2_row.iloc[0]['overview'], movie2_row.iloc[0]['original_language']

    selected_language_movies = df[df['original_language'].isin(selected_languages)]['overview'].tolist()

    emb1 = embed([movie1])
    emb2 = embed([movie2])
    neighbors1 = nn.kneighbors(emb1, return_distance=False)[0]
    neighbors2 = nn.kneighbors(emb2, return_distance=False)[0]

    popularity_recommendations1 = df[df['original_language'].isin(selected_languages)].nlargest(10, 'popularity')['id'].tolist()
    popularity_recommendations2 = df[df['original_language'].isin(selected_languages)].nlargest(10, 'popularity')['id'].tolist()

    combined_recommendations = list(set(popularity_recommendations1 + popularity_recommendations2 + df['id'].iloc[neighbors1].tolist() + df['id'].iloc[neighbors2].tolist()))

    return combined_recommendations

# Provide your test input values here
movie1_id = 354912
movie2_id = 497698
selected_languages = ["ja", "en"]
combined_recommendations = recommend(movie1_id, movie2_id, selected_languages)

# Print recommendations for testing
for recommendation in combined_recommendations:
    print(recommendation)
