interface Alert {
  id: string
  title: string
  alert_type: string
  severity: string
  status: string
  description: string
  created_at: string
}

interface AlertFeedProps {
  alerts: Alert[]
  onDismiss: (alertId: string) => void
}

export default function AlertFeed({ alerts, onDismiss }: AlertFeedProps) {
  const activeAlerts = alerts.filter((a) => a.status === 'active')

  return (
    <div>
      <h3 style={{ marginBottom: 12, fontSize: 16, fontWeight: 600 }}>
        Alerts {activeAlerts.length > 0 && <span style={{ color: '#f59e0b', fontSize: 13 }}>({activeAlerts.length} active)</span>}
      </h3>
      {alerts.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', color: '#94a3b8', padding: 32 }}>
          No alerts. Production is within normal parameters.
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {alerts.slice(0, 10).map((alert) => (
            <div
              key={alert.id}
              className="card"
              style={{
                padding: 12,
                borderLeft: `3px solid ${alert.severity === 'critical' ? '#ef4444' : alert.severity === 'high' ? '#f59e0b' : alert.severity === 'medium' ? '#f59e0b' : '#22c55e'}`,
                opacity: alert.status === 'dismissed' ? 0.5 : 1,
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <div style={{ fontWeight: 600, fontSize: 14 }}>{alert.title}</div>
                  <div style={{ color: '#94a3b8', fontSize: 12, marginTop: 2 }}>{alert.description}</div>
                  <div style={{ display: 'flex', gap: 6, marginTop: 6 }}>
                    <span className={`badge badge-${alert.severity}`}>{alert.severity}</span>
                    <span className={`badge badge-${alert.status}`}>{alert.status}</span>
                    <span style={{ color: '#64748b', fontSize: 11 }}>{new Date(alert.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
                {alert.status === 'active' && (
                  <button
                    className="btn-secondary"
                    style={{ padding: '4px 10px', fontSize: 12 }}
                    onClick={() => onDismiss(alert.id)}
                  >
                    Dismiss
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
