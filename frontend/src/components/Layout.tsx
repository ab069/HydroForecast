import { Outlet, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export default function Layout() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div>
      <header style={{ background: '#1e293b', borderBottom: '1px solid #334155', padding: '0 24px', height: 56, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{ fontSize: 20, fontWeight: 700, color: '#0d9488' }}>HydroForecast</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <span style={{ color: '#94a3b8', fontSize: 14 }}>{user?.name}</span>
          <button className="btn-secondary" onClick={handleLogout} style={{ padding: '6px 14px' }}>Logout</button>
        </div>
      </header>
      <main style={{ padding: 24, maxWidth: 1400, margin: '0 auto' }}>
        <Outlet />
      </main>
    </div>
  )
}
