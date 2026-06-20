const API_KEY = import.meta.env.VITE_TMDB_API_KEY;
const BASE = 'https://api.themoviedb.org/3';
const IMG = 'https://image.tmdb.org/t/p/w500';

// Convert raw TMDB movie object into card format
function toCard(movie) {
  return {
    id: movie.id,
    title: movie.title,
    rating: parseFloat(movie.vote_average.toFixed(1)),
    posterUrl: movie.poster_path ? `${IMG}${movie.poster_path}` : '',
  };
}

// Fetch 10 currently popular movies from TMDB's public API
export async function fetchPopular() {
  const res = await fetch(
    `${BASE}/movie/popular?api_key=${API_KEY}&language=en-US&page=1`
  );
  const data = await res.json();
  return data.results.slice(0, 10).map(toCard);
}

// Send a movie title to the FastAPI backend and return 10 content-based recommendations
export async function fetchRecommendations(query) {
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
    const res = await fetch(`${apiUrl}/api/recommend?query=${encodeURIComponent(query)}`);
    if (!res.ok) {
      if (res.status === 404) return null; // Movie not found
      throw new Error('Backend error');
    }
    return await res.json();
  } catch (err) {
    console.error("Failed to fetch recommendations:", err);
    return null;
  }
}
