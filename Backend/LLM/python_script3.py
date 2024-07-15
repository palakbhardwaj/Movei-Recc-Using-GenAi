import sys
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(model_url)

def embed(texts):
    return model(texts)

df = pd.read_csv("/home/pc/Desktop/Begining/webdev/HackOn/Final/Backend/LLM/updated_dataset.csv", engine="python")
df = df[["id", "overview", "popularity", "original_title", "original_language", "poster_url"]]  # Include "original_language" and "poster_url" in the data
df = df.dropna()
df = df.reset_index()
df = df[:500]

# Convert 'popularity' column to numeric
df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce')

# Check for any rows with non-numeric values in the 'popularity' column
non_numeric_rows = df[df['popularity'].isna()]
if not non_numeric_rows.empty:
    print("Warning: Some rows in the 'popularity' column contain non-numeric values and have been set to NaN.")
    print(non_numeric_rows)

titles = list(df['overview'])
embeddings = embed(titles)

nn = NearestNeighbors(n_neighbors=50)  # Increase the number of neighbors to 50
nn.fit(embeddings)

def recommend(movie1_id, movie2_id, selected_languages):
    movie1_row = df[df['id'] == movie1_id]
    movie2_row = df[df['id'] == movie2_id]

    if movie1_row.empty or movie2_row.empty:
        print('Invalid movie id(s).')
        return

    movie1, movie1_languages = movie1_row.iloc[0]['overview'], movie1_row.iloc[0]['original_language']
    movie2, movie2_languages = movie2_row.iloc[0]['overview'], movie2_row.iloc[0]['original_language']

    # Filter movies based on selected languages
    selected_language_movies = df[df['original_language'].isin(selected_languages)]['overview'].tolist()
    
    emb1 = embed([movie1])
    emb2 = embed([movie2])
    neighbors1 = nn.kneighbors(emb1, return_distance=False)[0]
    neighbors2 = nn.kneighbors(emb2, return_distance=False)[0]
    
    # Calculate recommendations based on popularity as well
    popularity_recommendations1 = df[df['original_language'].isin(selected_languages)].nlargest(10, 'popularity')[['id', 'poster_url']]
    popularity_recommendations2 = df[df['original_language'].isin(selected_languages)].nlargest(10, 'popularity')[['id', 'poster_url']]
    
    # Combine popularity-based recommendations with embeddings-based recommendations
    combined_recommendations = list(set(popularity_recommendations1['id'].tolist() + popularity_recommendations2['id'].tolist() + df['id'].iloc[neighbors1].tolist() + df['id'].iloc[neighbors2].tolist()))
    
    # Get the poster_url and id for each recommended movie ID
    recommendations_info = df[df['id'].isin(combined_recommendations)][['id', 'poster_url']]
    
    return recommendations_info.to_dict('records')  # Return a list of dictionaries containing 'id' and 'poster_url'

movie1_id = int(sys.argv[1])
movie2_id = int(sys.argv[2])
selected_languages = sys.argv[3:]  # Accept the list of selected languages
combined_recommendations = recommend(movie1_id, movie2_id, selected_languages)

# Print the recommended movie info (id and poster_url)
for recommendation in combined_recommendations:
    print(f"{recommendation['id']},{recommendation['poster_url']}")
