import numpy as np
import pandas as pd
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading dataset...")
# Load dataset
raw_movies = pd.read_csv('../data/400K_Movies.csv')

# Retain columns needed for ML and API response
movies = raw_movies[['id', 'title', 'overview', 'genres', 'keywords', 'directors', 'cast', 'poster_path', 'vote_average']].copy()

# Handle missing values
movies = movies.fillna('').drop_duplicates()

# Split comma-separated columns into lists and collapse multi-word names (e.g. "Tom Hanks" -> "TomHanks")
movies['genres']    = movies['genres'].apply(lambda x: [i.strip().replace(' ', '') for i in str(x).split(',') if i.strip()])
movies['keywords']  = movies['keywords'].apply(lambda x: [i.strip().replace(' ', '') for i in str(x).split(',') if i.strip()])
movies['cast']      = movies['cast'].apply(lambda x: [i.strip().replace(' ', '') for i in str(x).split(',') if i.strip()][:5])
movies['directors'] = movies['directors'].apply(lambda x: [i.strip().replace(' ', '') for i in str(x).split(',') if i.strip()])

# Stemming
ps = PorterStemmer()
def stem(text):
    return ' '.join([ps.stem(word) for word in str(text).split()])
movies['overview'] = movies['overview'].apply(stem).apply(lambda x: x.split())

# Build weighted tag string
movies['tags'] = (
    movies['overview'] +
    movies['genres'] * 3 +
    movies['keywords'] * 2 +
    movies['directors'] * 3 +
    movies['cast']
)
movies['tags'] = movies['tags'].apply(lambda x: ' '.join(x).lower())

print("Vectorizing...")
tv = TfidfVectorizer(
    max_features=10000,
    stop_words='english',
    min_df=2,
)
vectors = tv.fit_transform(movies['tags'])

print("Fitting KNN...")
nn = NearestNeighbors(
    n_neighbors=11,
    metric='cosine',
    algorithm='brute'
)
nn.fit(vectors)
print("Backend ready.")

@app.get("/api/recommend")
def recommend(query: str):
    # Find the movie matching the title (case insensitive)
    match = movies[movies['title'].str.lower() == query.lower()]
    
    if match.empty:
        raise HTTPException(status_code=404, detail="Movie not found")
        
    movie_index = match.index[0]
    movie_title = match.iloc[0]['title']
    
    distances, indices = nn.kneighbors(vectors[movie_index], n_neighbors=11)
    
    recs = []
    for i in indices[0][1:]:
        row = movies.iloc[i]
        poster_url = ""
        if row['poster_path']:
            poster_url = f"https://image.tmdb.org/t/p/w500{row['poster_path']}"
            
        # Extract float rating safely
        try:
            rating = float(row['vote_average'])
        except (ValueError, TypeError):
            rating = 0.0
            
        recs.append({
            "id": int(row['id']),
            "title": str(row['title']),
            "rating": round(rating, 1),
            "posterUrl": poster_url
        })
        
    return {
        "movieTitle": str(movie_title),
        "recs": recs
    }
