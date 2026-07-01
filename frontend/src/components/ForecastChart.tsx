import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface ForecastEntry {
  id: string
  forecast_date: string
  oil_rate_bpd: number
  gas_rate_mmscfd: number
  water_rate_bpd: number
  cumulative_oil_mmboe: number
  water_cut_pct: number
  gor: number
  days_on_production: number
}

interface ForecastChartProps {
  data: ForecastEntry[]
}

export default function ForecastChart({ data }: ForecastChartProps) {
  if (data.length === 0) {
    return (
      <div className="card" style={{ textAlign: 'center', color: '#94a3b8', padding: 32 }}>
        Select a reservoir with production data to view forecast chart.
      </div>
    )
  }

  const chartData = data.map((d) => ({
    date: new Date(d.forecast_date).toLocaleDateString(),
    oil: d.oil_rate_bpd,
    gas: d.gas_rate_mmscfd,
    water: d.water_rate_bpd,
    waterCut: d.water_cut_pct,
  }))

  return (
    <div className="card">
      <h3 style={{ marginBottom: 16, fontSize: 16, fontWeight: 600 }}>Production Forecast</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} />
          <YAxis stroke="#94a3b8" fontSize={12} />
          <Tooltip
            contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
            labelStyle={{ color: '#f1f5f9' }}
          />
          <Line type="monotone" dataKey="oil" stroke="#0d9488" name="Oil Rate (bpd)" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="gas" stroke="#f59e0b" name="Gas Rate (MMscfd)" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="water" stroke="#3b82f6" name="Water Rate (bpd)" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
