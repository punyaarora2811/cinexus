import { Star, ImageOff } from 'lucide-react';

export function MovieCard({ title, rating, posterUrl }) {
  return (
    <div className="group cursor-pointer">
      {/* Poster container */}
      <div className="relative overflow-hidden rounded-xl shadow-lg aspect-[2/3] bg-slate-800 transition-transform duration-300 group-hover:scale-[1.03] group-hover:shadow-2xl group-hover:shadow-purple-900/40 flex items-center justify-center">
        {posterUrl ? (
          <img
            src={posterUrl}
            alt={title}
            className="absolute inset-0 w-full h-full object-cover"
          />
        ) : (
          <div className="flex flex-col items-center justify-center p-4 text-center">
            <ImageOff className="w-10 h-10 text-slate-600 mb-2" />
            <span className="text-slate-500 text-xs font-medium uppercase tracking-widest">No Poster</span>
          </div>
        )}

        {/* Rating badge */}
        <div className="absolute top-2.5 right-2.5 flex items-center gap-0.5 bg-black/60 backdrop-blur-sm text-yellow-400 text-xs font-bold px-2 py-1 rounded-full">
          <Star className="w-3 h-3 fill-yellow-400" />
          {rating.toFixed(1)}
        </div>

      </div>

      <div className="mt-2.5 px-0.5">
        <h3 className="text-white font-medium text-sm truncate leading-tight">
          {title}
        </h3>
      </div>
    </div>
  );
}
