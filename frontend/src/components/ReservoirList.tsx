import { useState } from 'react'

interface Reservoir {
  id: string
  reservoir_name: string
  field_name: string
  reservoir_type: string
  depth_m: number
  porosity_pct: number
  permeability_md: number
  pressure_initial: number
  pressure_current: number
  temperature_c: number
  oil_in_place_mmboe: number
  gas_in_place_bcf: number
  recovery_factor_pct: number
}

interface ReservoirListProps {
  reservoirs: Reservoir[]
  onSelect: (id: string) => void
  selectedId?: string
}

function getRecoveryColor(rf: number): string {
  if (rf >= 40) return '#22c55e'
  if (rf >= 20) return '#f59e0b'
  return '#ef4444'
}

export default function ReservoirList({ reservoirs, onSelect, selectedId }: ReservoirListProps) {
  const [expanded, setExpanded] = useState<string | null>(null)

  return (
    <div>
      <h3 style={{ marginBottom: 12, fontSize: 16, fontWeight: 600 }}>Reservoirs</h3>
      {reservoirs.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', color: '#94a3b8', padding: 32 }}>
          No reservoirs yet. Add one above.
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {reservoirs.map((r) => (
            <div
              key={r.id}
              className="card"
              style={{
                padding: 12,
                cursor: 'pointer',
                borderColor: selectedId === r.id ? '#0d9488' : undefined,
              }}
              onClick={() => {
                setExpanded(expanded === r.id ? null : r.id)
                onSelect(r.id)
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontWeight: 600 }}>{r.reservoir_name}</div>
                  <div style={{ color: '#94a3b8', fontSize: 12 }}>{r.field_name} &middot; {r.reservoir_type}</div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{ fontSize: 13, color: getRecoveryColor(r.recovery_factor_pct), fontWeight: 600 }}>{r.recovery_factor_pct}% RF</span>
                  <span style={{ fontSize: 11, color: '#64748b' }}>{r.oil_in_place_mmboe} MMBOE</span>
                </div>
              </div>
              {expanded === r.id && (
                <div style={{ marginTop: 12, paddingTop: 12, borderTop: '1px solid #334155', display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8, fontSize: 12 }}>
                  <div><span style={{ color: '#94a3b8' }}>Pressure: </span>{r.pressure_current} psi</div>
                  <div><span style={{ color: '#94a3b8' }}>Porosity: </span>{r.porosity_pct}%</div>
                  <div><span style={{ color: '#94a3b8' }}>Permeability: </span>{r.permeability_md} mD</div>
                  <div><span style={{ color: '#94a3b8' }}>Depth: </span>{r.depth_m} m</div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
