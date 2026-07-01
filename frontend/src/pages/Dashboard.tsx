import { useEffect, useState } from 'react'
import { useHydroStore } from '../store/hydroStore'
import { useWebSocket } from '../hooks/useWebSocket'
import StatsCards from '../components/StatsCards'
import ReservoirForm from '../components/ReservoirForm'
import ReservoirList from '../components/ReservoirList'
import ForecastChart from '../components/ForecastChart'
import AlertFeed from '../components/AlertFeed'

export default function Dashboard() {
  const { reservoirs, forecasts, alerts, stats, fetchReservoirs, fetchForecasts, fetchAlerts, fetchStats, submitReservoir, updateAlertStatus } = useHydroStore()
  const [selectedReservoirId, setSelectedReservoirId] = useState<string | null>(null)
  const { analysis, report } = useWebSocket(selectedReservoirId)

  useEffect(() => {
    fetchReservoirs()
    fetchAlerts()
    fetchStats()
  }, [])

  useEffect(() => {
    if (selectedReservoirId) {
      fetchForecasts(selectedReservoirId)
    }
  }, [selectedReservoirId])

  const handleSubmitReservoir = async (data: any) => {
    await submitReservoir(data)
  }

  const handleDismissAlert = async (alertId: string) => {
    await updateAlertStatus(alertId, 'dismissed')
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {stats && (
        <StatsCards
          totalReservoirs={stats.total_reservoirs}
          totalOoip={stats.total_ooip_mmboe}
          avgRecovery={stats.avg_recovery_factor_pct}
          activeFields={stats.active_fields}
        />
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        <ReservoirForm onSubmit={handleSubmitReservoir} />
        <div>
          <ReservoirList reservoirs={reservoirs} onSelect={setSelectedReservoirId} selectedId={selectedReservoirId || undefined} />
        </div>
      </div>

      {selectedReservoirId && (
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 24 }}>
          <ForecastChart data={forecasts} />
          {analysis && (
            <div className="card">
              <h3 style={{ marginBottom: 12, fontSize: 16, fontWeight: 600 }}>Forecast Analysis</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8, fontSize: 13 }}>
                <div><span style={{ color: '#94a3b8' }}>Decline Type: </span>{analysis.decline_analysis.decline_type}</div>
                <div><span style={{ color: '#94a3b8' }}>Monthly Decline: </span>{analysis.decline_analysis.monthly_decline_pct}%</div>
                <div><span style={{ color: '#94a3b8' }}>Remaining Reserves: </span>{analysis.decline_analysis.remaining_reserves_mmboe} MMBOE</div>
                <div><span style={{ color: '#94a3b8' }}>Recovery Efficiency: </span>{analysis.recovery_analysis.efficiency}</div>
                <div><span style={{ color: '#94a3b8' }}>Water Breakthrough: </span>{analysis.water_breakthrough.water_breakthrough_detected ? 'Yes' : 'No'}</div>
                <div><span style={{ color: '#94a3b8' }}>Confidence: </span>{analysis.confidence}%</div>
              </div>
              {report && (
                <div style={{ marginTop: 12, paddingTop: 12, borderTop: '1px solid #334155' }}>
                  <details>
                    <summary style={{ color: '#0d9488', cursor: 'pointer', fontSize: 13 }}>View Full Report</summary>
                    <pre style={{ marginTop: 8, fontSize: 11, color: '#94a3b8', whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>{report}</pre>
                  </details>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      <AlertFeed alerts={alerts} onDismiss={handleDismissAlert} />
    </div>
  )
}
