<div align="center">
  <h1>🎬 Cinexus</h1>
  <p><strong>A dynamic, content-based movie recommendation engine built with React and Python.</strong></p>
  
  [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](#)
  [![Vite](https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E)](#)
  [![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](#)
  [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
  [![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)](#)
  [![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](#)
</div>

<br />

## 🌟 Overview

Cinexus is a full-stack web application that intelligently suggests movies based on content similarity. Utilizing the comprehensive TMDB dataset, it analyzes movie overviews, genres, keywords, cast, and directors to uncover the 10 closest recommendations to your favorite films via cosine similarity.

## ✨ Features

- **Smart Recommendations:** Leverages TF-IDF vectorization and K-Nearest Neighbors (KNN) to generate accurate, content-based movie recommendations.
- **Beautiful UI:** A responsive, visually striking frontend crafted with React, Vite, and Tailwind CSS.
- **Lightning Fast API:** A robust backend powered by FastAPI that serves predictions rapidly.
- **Rich Data Processing:** Incorporates NLTK for text stemming and scikit-learn for machine learning pipelines.

## 📂 Project Structure

```text
cinexus/
├── backend/
│   ├── main.py                   # FastAPI application & ML pipeline
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── public/                   # Static assets (favicon)
│   ├── src/
│   │   ├── components/           # Reusable React components
│   │   ├── lib/                  # Helper functions & API utilities
│   │   ├── styles/               # Global styling (Tailwind CSS v4)
│   │   ├── App.jsx               # Main application component
│   │   └── main.jsx              # React application entry point
│   ├── .env.example              # Environment variables template
│   ├── index.html                # HTML entry point
│   ├── package.json              # Frontend dependencies
│   └── vite.config.js            # Vite configuration
├── data/
│   └── 400K_Movies.csv           # TMDB 400k dataset (gitignored)
├── .gitignore
├── package.json                  # Root monorepo scripts
├── render.yaml                   # Render deployment blueprint
└── README.md
```

## 🚀 Getting Started

Follow these instructions to set up the project locally.

### Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **TMDB API Key** (Get one for free [here](https://www.themoviedb.org/settings/api))

### 1. Clone the Repository

```bash
git clone https://github.com/punyaarora2811/cinexus.git
cd cinexus
```

### 2. Download the Dataset (Local Dev Only)

> **Note:** If you're deploying to Render, skip this step — the dataset is downloaded automatically during the build.

Download the TMDB 400k dataset from [Kaggle](https://www.kaggle.com/datasets/ggtejas/tmdb-imdb-merged-movies-dataset) and place it in the `data` directory:

```bash
# Ensure the structure looks like this:
data/400K_Movies.csv
```

### 3. Backend Setup (FastAPI & ML)

Install the Python dependencies and start the backend server. The model will build its vectors on startup (takes a few seconds).

```bash
# Install backend dependencies
npm run install:backend

# Start the FastAPI server (Runs on http://127.0.0.1:8000)
npm run dev:backend
```

### 4. Frontend Setup (React UI)

Configure the environment variables and start the frontend application.

```bash
# Set up your environment variables
cp frontend/.env.example frontend/.env

# Edit frontend/.env and add your TMDB API Key:
# VITE_TMDB_API_KEY=your_api_key_here

# Install dependencies and start the dev server
npm run install:frontend
npm run dev:frontend
```

The frontend will be available at `http://localhost:5173` (or similar, check terminal output).

## 🧠 How the ML Pipeline Works

1. **Data Preprocessing:** Cleans the TMDB dataset by handling missing values and dropping duplicates.
2. **Feature Extraction:** Consolidates genres, keywords, cast (top 5), and directors into robust lists. Multi-word names are collapsed (e.g., `Tom Hanks` → `TomHanks`) to prevent false positive matches on shared first names.
3. **Text Normalization:** Applies stemming to the movie overviews using NLTK so that word variations map to the same token.
4. **Weighted Tagging:** Constructs a master "tag" string for each movie where directors and genres are weighted 3×, keywords 2×, and overview/cast 1×.
5. **Vectorization:** Converts the tags into a numerical matrix using TF-IDF, effectively down-weighting common tokens and boosting rare discriminative ones.
6. **Recommendation:** Computes the closest neighbors via Cosine Similarity utilizing the K-Nearest Neighbors (KNN) algorithm.

## 🚀 Deployment (Render)

This project includes a [`render.yaml`](render.yaml) blueprint for one-click deployment to [Render](https://render.com).

1. Push your code to GitHub.
2. Sign in to Render and click **New > Blueprint**.
3. Connect your repository — Render will automatically detect the blueprint and provision both services:
   - **cinexus-backend** → Python Web Service
   - **cinexus-frontend** → Static Site
4. Add the following environment variable to the **cinexus-backend** service:
   | Key | Value | Purpose |
   |---|---|---|
   | `KAGGLE_API_TOKEN` | Your Kaggle API token | Allows the build to download the 400K dataset automatically |
5. Add the following environment variable to the **cinexus-frontend** service:
   | Key | Value | Purpose |
   |---|---|---|
   | `VITE_TMDB_API_KEY` | Your TMDB API key | Required for fetching popular movies and poster images |

> **Note:** The 279 MB dataset is `.gitignored` to comply with GitHub's file size limits. The `render.yaml` build command automatically downloads it from Kaggle, so you never need to push it to Git.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
