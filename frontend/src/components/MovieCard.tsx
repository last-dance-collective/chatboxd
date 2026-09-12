import type { MovieCardData } from '../types'

function badgeClass(index: number): string {
  if (index === 0) return 'badge badge-imdb'
  if (index === 1) return 'badge badge-rt'
  return 'badge badge-mc'
}

function badgeLabel(source: string | undefined, index: number): string {
  if (source?.toLowerCase().includes('imdb')) return 'IMDB'
  if (source?.toLowerCase().includes('rotten')) return 'RT'
  if (source?.toLowerCase().includes('metacritic')) return 'MC'
  if (index === 0) return 'IMDB'
  if (index === 1) return 'RT'
  return 'MC'
}

export function MovieCard({ movie }: { movie: MovieCardData }) {
  return (
    <article className="movie-card">
      <a href={movie.url} target="_blank" rel="noreferrer">
        <img className="movie-card-img" src={movie.image_url} alt={movie.title} />
      </a>
      <div className="movie-card-body">
        <h3>
          <a href={movie.url} target="_blank" rel="noreferrer">
            {movie.title}
          </a>
        </h3>
        {movie.ratings.length > 0 && (
          <div className="ratings">
            {movie.ratings.map((rating, index) => (
              <span className={badgeClass(index)} key={`${rating.Source}-${index}`}>
                {badgeLabel(rating.Source, index)}: {rating.Value}
              </span>
            ))}
          </div>
        )}
        {movie.plot ? <p>{movie.plot}</p> : null}
      </div>
    </article>
  )
}
