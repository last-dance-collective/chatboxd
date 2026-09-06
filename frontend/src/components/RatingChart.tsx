import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

const BINS = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

function bucket(value: number): number {
  return Math.round(value * 2) / 2
}

export function RatingChart({ ratings }: { ratings: number[] }) {
  const counts = new Map<number, number>(BINS.map((bin) => [bin, 0]))
  for (const rating of ratings) {
    const key = bucket(rating)
    counts.set(key, (counts.get(key) ?? 0) + 1)
  }
  const data = BINS.map((bin) => ({ rating: String(bin), count: counts.get(bin) ?? 0 }))

  if (ratings.length === 0) {
    return <p className="muted">No ratings to display.</p>
  }

  return (
    <div className="chart-wrap">
      <h3 className="chart-title">Histogram of movie ratings</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data}>
          <CartesianGrid stroke="rgba(204, 219, 233, 0.12)" vertical={false} />
          <XAxis dataKey="rating" stroke="#9ab" tick={{ fill: '#ccdbe9', fontSize: 12 }} />
          <YAxis allowDecimals={false} stroke="#9ab" tick={{ fill: '#ccdbe9', fontSize: 12 }} />
          <Tooltip
            contentStyle={{
              background: '#2c3440',
              border: '1px solid #456',
              borderRadius: 8,
              color: '#fff',
            }}
          />
          <Bar dataKey="count" fill="#00e054" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
