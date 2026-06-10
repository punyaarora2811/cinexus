import numpy as np
import pandas as pd
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Load dataset
movies = pd.read_csv('data/400K_Movies.csv')

# Retain only the columns that carry meaningful content signal
movies = movies[['id', 'title', 'overview', 'genres', 'keywords', 'directors', 'cast']]

# Missing values become empty strings so string operations don't fail
movies = movies.fillna('').drop_duplicates()

# Split comma-separated columns into lists
movies['genres']    = movies['genres'].apply(lambda x: [i.strip() for i in x.split(',')])
movies['keywords']  = movies['keywords'].apply(lambda x: [i.strip() for i in x.split(',')])
movies['cast']      = movies['cast'].apply(lambda x: [i.strip() for i in x.split(',')])
movies['directors'] = movies['directors'].apply(lambda x: [i.strip() for i in x.split(',')])

# Stemming reduces words to their root form so variations like act, acting, acted all map to the same token
# We only stem the overview (plot description) and leave names untouched — stemming proper nouns produces garbage tokens
ps = PorterStemmer()
def stem(text):
    return ' '.join([ps.stem(word) for word in text.split()])
movies['overview'] = movies['overview'].apply(stem).apply(lambda x: x.split())

# Collapse multi-word names into single tokens
# Without this, "Tom Hanks" becomes two tokens "tom" and "hanks", causing unrelated movies that share a first name to appear similar
movies['genres']    = movies['genres'].apply(lambda x: [i.replace(' ', '') for i in x])
movies['keywords']  = movies['keywords'].apply(lambda x: [i.replace(' ', '') for i in x])
movies['cast']      = movies['cast'].apply(lambda x: [i.replace(' ', '') for i in x[:5]])  # top 5 actors only
movies['directors'] = movies['directors'].apply(lambda x: [i.replace(' ', '') for i in x])

# Build weighted tag string
# Directors and genres are repeated 3× and keywords 2× so TF-IDF assigns them higher importance during similarity scoring
movies['tags'] = (
    movies['overview'] +
    movies['genres'] * 3 +
    movies['keywords'] * 2 +
    movies['directors'] * 3 +
    movies['cast']
)
movies = movies[['id', 'title', 'tags']]
movies['tags'] = movies['tags'].apply(lambda x: ' '.join(x).lower())

# TF-IDF Vectorization
# TF-IDF down-weights tokens that appear across many movies and boosts rare tokens (e.g. a niche genre or specific director)
tv = TfidfVectorizer(
    max_features=10000,   # vocabulary capped at the 10k most informative tokens
    stop_words='english', # common words like is, am, are removed — they add noise
    min_df=2,             # tokens appearing in only one movie are likely noise
)
vectors = tv.fit_transform(movies['tags'])

# K-Nearest Neighbors Model
# Cosine similarity measures the angle between two tag vectors as movies with the same vocabulary profile point in the same direction regardless of length
nn = NearestNeighbors(
    n_neighbors=11,   # 1 (the query movie itself) + 10 recommendations
    metric='cosine',
    algorithm='brute'
)
nn.fit(vectors)

# Recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0] # find the input's index in dataframe
    distances, indices = nn.kneighbors(vectors[movie_index], n_neighbors=11) # calculate the distances and indices of the nearest 11 neighbours
    for i in indices[0][1:]: 
        print(movies.iloc[i]['title']) # print the title of the recieved indices except the 1st one as its the movie itself

# Main function
if __name__ == '__main__':
    movie = input('Enter a movie title: ').strip()
    recommend(movie)