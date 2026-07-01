interface StatsCardsProps {
  totalReservoirs: number
  totalOoip: number
  avgRecovery: number
  activeFields: number
}

export default function StatsCards({ totalReservoirs, totalOoip, avgRecovery, activeFields }: StatsCardsProps) {
  const cards = [
    { label: 'Total Reservoirs', value: totalReservoirs, color: '#0d9488' },
    { label: 'Total OOIP (MMBOE)', value: totalOoip.toLocaleString(), color: '#14b8a6' },
    { label: 'Avg Recovery Factor', value: `${avgRecovery}%`, color: '#22c55e' },
    { label: 'Active Fields', value: activeFields, color: '#f59e0b' },
  ]

  return (
    <div className="grid grid-4">
      {cards.map((card) => (
        <div key={card.label} className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: 28, fontWeight: 700, color: card.color }}>{card.value}</div>
          <div style={{ color: '#94a3b8', fontSize: 13, marginTop: 4 }}>{card.label}</div>
        </div>
      ))}
    </div>
  )
}
