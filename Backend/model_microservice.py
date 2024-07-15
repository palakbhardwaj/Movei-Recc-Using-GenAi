# from fastapi import FastAPI, Body
# from typing import List
# import joblib
# import numpy as np
# import pandas as pd
# from sklearn.neighbors import NearestNeighbors
# import tensorflow_hub as hub

# app = FastAPI()

# # Load the trained model
# nn = joblib.load('movie_recommender_model.pkl')

# # Load the movie data from a CSV file
# df = pd.read_csv('updated_dataset.csv')

# # Convert 'popularity' column to numeric
# df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce')

# # Check for any rows with non-numeric values in the 'popularity' column
# non_numeric_rows = df[df['popularity'].isna()]
# if not non_numeric_rows.empty:
#     print("Warning: Some rows in the 'popularity' column contain non-numeric values and have been set to NaN.")
#     print(non_numeric_rows)

# # Load the TensorFlow Hub model
# model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
# model = hub.load(model_url)

# # Define the FastAPI route for movie recommendations
# # Define the FastAPI route for movie recommendations
# @app.post("/recommend/")
# async def recommend(
#     movie1_id: int = Body(...),
#     movie2_id: int = Body(...),
#     selected_languages: List[str] = Body(...),
# ):
#     def embed(texts):
#         return model(texts)

#     # Recommendation logic using the loaded model
#     movie1_row = df[df['id'] == movie1_id]
#     movie2_row = df[df['id'] == movie2_id]

#     if movie1_row.empty or movie2_row.empty:
#         return {"error": "Invalid movie id(s)"}

#     movie1, movie1_languages = movie1_row.iloc[0]['overview'], movie1_row.iloc[0]['original_language']
#     movie2, movie2_languages = movie2_row.iloc[0]['overview'], movie2_row.iloc[0]['original_language']

#     # Filter movies based on selected languages
#     selected_language_movies = df[df['original_language'].isin(selected_languages)]['overview'].tolist()

#     emb1 = embed([movie1])
#     emb2 = embed([movie2])
#     neighbors1 = nn.kneighbors(emb1, return_distance=False)[0]
#     neighbors2 = nn.kneighbors(emb2, return_distance=False)[0]

#     # Calculate recommendations based on popularity as well
#     popularity_recommendations1 = df[df['original_language'].isin(selected_languages)].nlargest(10, 'popularity')[['id', 'poster_url']]
#     popularity_recommendations2 = df[df['original_language'].isin(selected_languages)].nlargest(10, 'popularity')[['id', 'poster_url']]

#     # Combine popularity-based recommendations with embeddings-based recommendations
#     combined_recommendations = list(set(popularity_recommendations1['id'].tolist() + popularity_recommendations2['id'].tolist() + df['id'].iloc[neighbors1].tolist() + df['id'].iloc[neighbors2].tolist()))

#     # Filter recommendations by selected language
#     recommendations_info = df[df['id'].isin(combined_recommendations) & df['original_language'].isin(selected_languages)][['id', 'poster_url']]

#     return recommendations_info.to_dict('records')

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI, Body
from typing import List
import joblib
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import tensorflow_hub as hub

app = FastAPI()

# Load the trained model
nn = joblib.load('movie_recommender_model.pkl')

# Load the movie data from a CSV file
df = pd.read_csv('updated_dataset.csv')

# Convert 'popularity' column to numeric
df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce')

# Check for any rows with non-numeric values in the 'popularity' column
non_numeric_rows = df[df['popularity'].isna()]
if not non_numeric_rows.empty:
    print("Warning: Some rows in the 'popularity' column contain non-numeric values and have been set to NaN.")
    print(non_numeric_rows)

# Load the TensorFlow Hub model
model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(model_url)

# Define the FastAPI route for movie recommendations
@app.post("/recommend/")
async def recommend(
    movie1: int = Body(...),
    movie2: int = Body(...),
    languages: List[str] = Body(...),
    adult: int = Body(...),
):
    def embed(texts):
        return model(texts)

    # Recommendation logic using the loaded model
    movie1_row = df[df['id'] == movie1]
    movie2_row = df[df['id'] == movie2]

    if movie1_row is None or movie2_row is None:
        return {"error": "Invalid movie id(s)"}

    movie1, movie1_languages = movie1_row.iloc[0]['overview'], movie1_row.iloc[0]['original_language']
    movie2, movie2_languages = movie2_row.iloc[0]['overview'], movie2_row.iloc[0]['original_language']

    # Filter movies based on selected languages
    selected_language_movies = df[df['original_language'].isin(languages)]['overview'].tolist()

    emb1 = embed([movie1])
    emb2 = embed([movie2])
    neighbors1 = nn.kneighbors(emb1, return_distance=False)[0]
    neighbors2 = nn.kneighbors(emb2, return_distance=False)[0]

    # Calculate recommendations based on popularity as well
    popularity_recommendations1 = df[df['original_language'].isin(languages)].nlargest(10, 'popularity')[['id', 'poster_url']]
    popularity_recommendations2 = df[df['original_language'].isin(languages)].nlargest(10, 'popularity')[['id', 'poster_url']]

    # Combine popularity-based recommendations with embeddings-based recommendations
    combined_recommendations = list(set(popularity_recommendations1['id'].tolist() + popularity_recommendations2['id'].tolist() + df['id'].iloc[neighbors1].tolist() + df['id'].iloc[neighbors2].tolist()))

    # Filter recommendations by selected language
    recommendations_info = df[df['id'].isin(combined_recommendations) & df['original_language'].isin(languages)][['id', 'poster_url']]

    # Add a filter for family-friendly movies and adult content
    if not adult:
        family_friendly_recommendations = df[df['genre'].str.contains('Family')]

        recommendations_info = recommendations_info[recommendations_info['id'].isin(family_friendly_recommendations['id'])]

    return {"recommendations": recommendations_info.to_dict('records')}  # Corrected indentation

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)