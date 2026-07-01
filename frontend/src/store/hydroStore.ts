import { create } from 'zustand'
import axios from 'axios'

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
  created_at: string
}

interface ForecastEntry {
  id: string
  reservoir_id: string
  forecast_date: string
  oil_rate_bpd: number
  gas_rate_mmscfd: number
  water_rate_bpd: number
  cumulative_oil_mmboe: number
  cumulative_gas_bcf: number
  water_cut_pct: number
  gor: number
  days_on_production: number
}

interface Alert {
  id: string
  reservoir_id: string
  title: string
  alert_type: string
  severity: string
  status: string
  description: string
  created_at: string
}

interface Stats {
  total_reservoirs: number
  total_ooip_mmboe: number
  avg_recovery_factor_pct: number
  active_fields: number
}

interface HydroState {
  reservoirs: Reservoir[]
  forecasts: ForecastEntry[]
  alerts: Alert[]
  stats: Stats | null
  loading: boolean
  fetchReservoirs: () => Promise<void>
  fetchForecasts: (reservoirId?: string) => Promise<void>
  fetchAlerts: () => Promise<void>
  fetchStats: () => Promise<void>
  submitReservoir: (data: any) => Promise<void>
  submitForecast: (data: any) => Promise<void>
  updateAlertStatus: (alertId: string, status: string) => Promise<void>
}

const api = () => {
  const token = localStorage.getItem('token')
  return axios.create({ headers: { Authorization: `Bearer ${token}` } })
}

export const useHydroStore = create<HydroState>((set, get) => ({
  reservoirs: [],
  forecasts: [],
  alerts: [],
  stats: null,
  loading: false,
  fetchReservoirs: async () => {
    const { data } = await api().get('/api/reservoirs')
    set({ reservoirs: data })
  },
  fetchForecasts: async (reservoirId?: string) => {
    const url = reservoirId ? `/api/forecasts?reservoir_id=${reservoirId}` : '/api/forecasts'
    const { data } = await api().get(url)
    set({ forecasts: data })
  },
  fetchAlerts: async () => {
    const { data } = await api().get('/api/alerts')
    set({ alerts: data })
  },
  fetchStats: async () => {
    const { data } = await api().get('/api/reservoirs/stats')
    set({ stats: data })
  },
  submitReservoir: async (formData) => {
    await api().post('/api/reservoirs', formData)
    await get().fetchReservoirs()
    await get().fetchStats()
  },
  submitForecast: async (formData) => {
    await api().post('/api/forecasts', formData)
    await get().fetchForecasts(formData.reservoir_id)
  },
  updateAlertStatus: async (alertId, status) => {
    await api().put(`/api/alerts/${alertId}`, { status })
    await get().fetchAlerts()
  },
}))
