# Movie Recommender System

A content-based movie recommender built on the TMDB 400k dataset using TF-IDF vectorization and K-Nearest Neighbors.

## How it works

1. Loads and cleans the TMDB dataset — fills missing values, drops duplicates
2. Splits genres, keywords, cast, and directors from comma-separated strings into lists
3. Stems overview words so variations like *act*, *acting*, *acted* map to the same token
4. Collapses multi-word names into single tokens (e.g. `Tom Hanks` → `TomHanks`) to avoid false matches on shared first names
5. Builds a weighted tag string per movie — directors and genres repeated 3×, keywords 2×, overview and cast 1×
6. Vectorizes tags with TF-IDF — down-weights common tokens, boosts rare discriminative ones
7. Finds the 10 nearest neighbors by cosine similarity using KNN

## Setup

```bash
git clone https://github.com/punyaarora2811/cinexus.git
cd cinexus
pip install -r requirements.txt
```

Download the TMDB 400k dataset from [Kaggle](https://www.kaggle.com/datasets/ggtejas/tmdb-imdb-merged-movies-dataset) and place it at:

```
data/400K_Movies.csv
```

## Usage

```bash
python recommender.py
# Enter a movie title: Inception
```

## Project structure

| File | Description |
|---|---|
| `recommender.py` | Full pipeline — preprocessing, model, and recommendation |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |
| `.gitignore` | Excludes dataset and system files from git |

## Tech stack

- Python, Pandas, NumPy
- scikit-learn — TF-IDF vectorization, K-Nearest Neighbors
- NLTK — Porter Stemmer
