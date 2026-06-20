import gc
import pandas as pd
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ── FastAPI Setup ──────────────────────────────────────────────────────────────

app = FastAPI()

# Allow cross-origin requests so the frontend can call this API from any domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Data Loading & Cleaning ───────────────────────────────────────────────────

print("Loading dataset...")

# Load only the columns needed for ML features and API responses
raw_movies = pd.read_csv(
    '../data/400K_Movies.csv',
    usecols=['id', 'title', 'overview', 'genres', 'keywords', 'directors', 'cast', 'poster_path', 'vote_average']
)

# Fill missing values with empty strings and remove duplicate movie IDs
movies = raw_movies.fillna('').drop_duplicates(subset='id')
del raw_movies
gc.collect()

# Remove movies that have no overview and no genres (useless for recommendations)
movies = movies[
    (movies['overview'].str.strip() != '') | (movies['genres'].str.strip() != '')
]

# Keep only the top 50K movies by rating to fit within Render's 512 MB free tier
movies['vote_average'] = pd.to_numeric(movies['vote_average'], errors='coerce').fillna(0)
movies = movies.nlargest(50000, 'vote_average').reset_index(drop=True)
gc.collect()

print(f"Working with {len(movies)} movies after filtering...")

# ── Feature Engineering ───────────────────────────────────────────────────────

# Convert comma-separated strings into lists; collapse multi-word names
# (e.g. "Tom Hanks" -> "TomHanks") to prevent false matches on shared first names
movies['genres']    = movies['genres'].apply(lambda x: [i.strip().replace(' ', '') for i in str(x).split(',') if i.strip()])
movies['keywords']  = movies['keywords'].apply(lambda x: [i.strip().replace(' ', '') for i in str(x).split(',') if i.strip()])
movies['cast']      = movies['cast'].apply(lambda x: [i.strip().replace(' ', '') for i in str(x).split(',') if i.strip()][:5])
movies['directors'] = movies['directors'].apply(lambda x: [i.strip().replace(' ', '') for i in str(x).split(',') if i.strip()])

# Apply Porter stemming to overviews so word variations (e.g. "running" -> "run") share the same token
ps = PorterStemmer()
def stem(text):
    return ' '.join([ps.stem(word) for word in str(text).split()])
movies['overview'] = movies['overview'].apply(stem).apply(lambda x: x.split())

# Build a weighted tag string per movie: directors & genres count 3x, keywords 2x, overview & cast 1x
movies['tags'] = (
    movies['overview'] +
    movies['genres'] * 3 +
    movies['keywords'] * 2 +
    movies['directors'] * 3 +
    movies['cast']
)
movies['tags'] = movies['tags'].apply(lambda x: ' '.join(x).lower())

# Free the intermediate feature columns — only tags, id, title, poster_path, vote_average remain
movies = movies.drop(columns=['overview', 'genres', 'keywords', 'directors', 'cast'])
gc.collect()

# ── Model Training ────────────────────────────────────────────────────────────

# Convert tag strings into a TF-IDF numerical matrix (sparse) for similarity comparison
print("Vectorizing...")
tv = TfidfVectorizer(
    max_features=5000,
    stop_words='english',
    min_df=2,
)
vectors = tv.fit_transform(movies['tags'])

# Free the tags column — the TF-IDF matrix has replaced it
movies = movies.drop(columns=['tags'])
gc.collect()

# Fit a KNN model using cosine distance to find the 10 most similar movies (+ 1 for the query itself)
print("Fitting KNN...")
nn = NearestNeighbors(
    n_neighbors=11,
    metric='cosine',
    algorithm='brute'
)
nn.fit(vectors)
print(f"Backend ready. {len(movies)} movies loaded.")

# ── API Endpoint ──────────────────────────────────────────────────────────────

@app.get("/api/recommend")
def recommend(query: str):
    """Accept a movie title and return 10 similar movies based on content similarity."""

    # Case-insensitive title lookup
    match = movies[movies['title'].str.lower() == query.lower()]
    
    if match.empty:
        raise HTTPException(status_code=404, detail="Movie not found")
        
    movie_index = match.index[0]
    movie_title = match.iloc[0]['title']
    
    # Find the 11 nearest neighbors (first result is the query movie itself, so skip it)
    distances, indices = nn.kneighbors(vectors[movie_index], n_neighbors=11)
    
    # Build the response list with poster URLs and ratings
    recs = []
    for i in indices[0][1:]:
        row = movies.iloc[i]
        poster_url = ""
        if row['poster_path']:
            poster_url = f"https://image.tmdb.org/t/p/w500{row['poster_path']}"
            
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
