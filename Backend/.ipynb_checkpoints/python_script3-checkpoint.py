import sys
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pandas as pd
import joblib
from sklearn.neighbors import NearestNeighbors

model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(model_url)

def embed(texts):
    return model(texts)

df = pd.read_csv("/home/pc/Desktop/Begining/webdev/HackOn/Final/Backend/updated_dataset.csv", engine="python")
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

# Save the trained model to a .pkl file
joblib.dump(nn, 'movie_recommender_model.pkl')

