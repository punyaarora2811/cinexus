import { Search, Film, Clapperboard, Loader2 } from 'lucide-react';
import { useState, useEffect } from 'react';
import { MovieCard } from './components/MovieCard';
import { fetchPopular, fetchRecommendations } from './lib/tmdb';

const BG_IMAGE =
  'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwyfHxkYXJrJTIwY2luZW1hJTIwdGhlYXRlciUyMGZpbG0lMjBkcmFtYXRpY3xlbnwxfHx8fDE3ODE2OTg1MTh8MA&ixlib=rb-4.1.0&q=80&w=1920';

export default function App() {
  const [query, setQuery] = useState('');
  const [movies, setMovies] = useState([]);
  const [mode, setMode] = useState('popular');
  const [basedOn, setBasedOn] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch popular movies on initial load
  useEffect(() => {
    fetchPopular()
      .then(setMovies)
      .catch(() => setError('Could not load movies. Check your API key.'))
      .finally(() => setLoading(false));
  }, []);

  // Send the query to the FastAPI backend and display content-based recommendations
  async function handleRecommend() {
    if (!query.trim()) return;
    setLoading(true);
    setError('');
    
    try {
      const result = await fetchRecommendations(query.trim());

      if (!result || result.recs.length === 0) {
        setError(`No recommendations found for "${query}". Try a different title.`);
        return;
      }

      setMovies(result.recs);
      setBasedOn(result.movieTitle);
      setMode('recommendations');
    } catch {
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  // Reset to popular movies grid
  async function handleBackToPopular() {
    setMode('popular');
    setQuery('');
    setLoading(true);
    
    try {
      const popular = await fetchPopular();
      setMovies(popular);
    } catch {
      setError('Could not load movies.');
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter') handleRecommend();
  }

  return (
    <div className="min-h-screen relative" style={{ fontFamily: "'Inter', sans-serif" }}>
      {/* Background styling */}
      <div
        className="fixed inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${BG_IMAGE})` }}
      />
      <div className="fixed inset-0 bg-gradient-to-b from-black/85 via-slate-950/90 to-slate-950" />

      <div className="relative z-10">
        {/* Navigation */}
        <nav className="flex items-center justify-center px-10 py-5 border-b border-white/5 backdrop-blur-sm relative">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-purple-600 flex items-center justify-center">
              <Clapperboard className="w-4 h-4 text-white" />
            </div>
            <span
              className="text-3xl text-white uppercase"
              style={{ fontFamily: "'Bebas Neue', sans-serif", letterSpacing: '0.14em' }}
            >
              Cinexus
            </span>
          </div>
          <p className="absolute right-10 text-gray-500 text-xs tracking-widest uppercase">
            AI Movie Recommendations
          </p>
        </nav>

        {/* Hero Section & Search Input */}
        <div className="pt-16 pb-14 px-10 text-center">
          <h1
            className="text-white mb-3 uppercase"
            style={{
              fontFamily: "'Bebas Neue', sans-serif",
              fontSize: '4.5rem',
              letterSpacing: '0.06em',
              lineHeight: 1,
            }}
          >
            Type a movie.{' '}
            <span
              className="text-transparent bg-clip-text"
              style={{ backgroundImage: 'linear-gradient(135deg, #a855f7, #ec4899)' }}
            >
              Discover ten.
            </span>
          </h1>
          <p className="text-gray-400 text-sm max-w-xs mx-auto mb-10">
            Enter any film you love and we'll surface ten recommendations worth your time.
          </p>

          <div className="max-w-xl mx-auto relative">
            <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
              <Search className="w-5 h-5 text-gray-400" />
            </div>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="e.g. Interstellar, The Godfather, Parasite…"
              className="w-full pl-12 pr-36 py-3.5 bg-white/10 backdrop-blur-md border border-white/15 rounded-full text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-sm"
            />
            <button
              onClick={handleRecommend}
              disabled={loading || !query.trim()}
              className="absolute inset-y-1.5 right-1.5 px-5 bg-purple-600 hover:bg-purple-500 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-semibold rounded-full transition-colors"
            >
              Recommend
            </button>
          </div>
        </div>

        {/* Section Label */}
        <div className="px-10 pb-5">
          <div className="max-w-7xl mx-auto flex items-center gap-3">
            <Film className="w-4 h-4 text-purple-400" />
            <span
              className="text-white text-lg uppercase tracking-widest"
              style={{ fontFamily: "'Bebas Neue', sans-serif" }}
            >
              {mode === 'popular' ? 'Currently Popular' : 'Recommendations'}
            </span>
            {mode === 'recommendations' && basedOn && (
              <span className="text-gray-500 text-xs">based on "{basedOn}"</span>
            )}
            <div className="flex-1 h-px bg-white/8 ml-2" />
            {mode === 'recommendations' && (
              <button
                onClick={handleBackToPopular}
                className="text-gray-500 hover:text-purple-400 text-xs transition-colors"
              >
                ← Back to popular
              </button>
            )}
            {!loading && <span className="text-gray-500 text-xs">10 picks</span>}
          </div>
        </div>

        {/* Movie Grid */}
        <div className="px-10 pb-20">
          <div className="max-w-7xl mx-auto">
            {loading ? (
              <div className="flex items-center justify-center py-32">
                <Loader2 className="w-8 h-8 text-purple-400 animate-spin" />
              </div>
            ) : error ? (
              <div className="flex items-center justify-center py-32">
                <p className="text-gray-400 text-sm">{error}</p>
              </div>
            ) : (
              <div className="grid grid-cols-5 gap-5">
                {movies.map((movie) => (
                  <MovieCard
                    key={movie.id}
                    title={movie.title}
                    rating={movie.rating}
                    posterUrl={movie.posterUrl}
                  />
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-white/5 px-10 py-6">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <span
              className="text-gray-600 text-xs tracking-widest uppercase"
              style={{ fontFamily: "'Bebas Neue', sans-serif" }}
            >
              Cinexus © 2025
            </span>
            <span className="text-gray-700 text-xs">Powered by TMDB</span>
          </div>
        </div>
      </div>
    </div>
  );
}
