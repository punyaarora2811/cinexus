import { Star } from 'lucide-react';

export function MovieCard({ title, rating, posterUrl }) {
  return (
    <div className="group cursor-pointer">
      {/* Poster container */}
      <div className="relative overflow-hidden rounded-xl shadow-lg aspect-[2/3] bg-slate-800 transition-transform duration-300 group-hover:scale-[1.03] group-hover:shadow-2xl group-hover:shadow-purple-900/40">
        <img
          src={posterUrl}
          alt={title}
          className="absolute inset-0 w-full h-full object-cover"
        />

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
