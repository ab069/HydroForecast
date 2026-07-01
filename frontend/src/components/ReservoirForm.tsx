import { useState } from 'react'

interface ReservoirFormProps {
  onSubmit: (data: any) => Promise<void>
}

export default function ReservoirForm({ onSubmit }: ReservoirFormProps) {
  const [form, setForm] = useState({
    reservoir_name: '',
    field_name: '',
    reservoir_type: 'oil',
    depth_m: 0,
    porosity_pct: 0,
    permeability_md: 0,
    pressure_initial: 0,
    oil_in_place_mmboe: 0,
    gas_in_place_bcf: 0,
    recovery_factor_pct: 0,
  })
  const [saving, setSaving] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: ['depth_m', 'porosity_pct', 'permeability_md', 'pressure_initial', 'oil_in_place_mmboe', 'gas_in_place_bcf', 'recovery_factor_pct'].includes(name) ? parseFloat(value) || 0 : value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    await onSubmit(form)
    setForm({
      reservoir_name: '', field_name: '', reservoir_type: 'oil',
      depth_m: 0, porosity_pct: 0, permeability_md: 0, pressure_initial: 0,
      oil_in_place_mmboe: 0, gas_in_place_bcf: 0, recovery_factor_pct: 0,
    })
    setSaving(false)
  }

  return (
    <form onSubmit={handleSubmit} className="card">
      <h3 style={{ marginBottom: 16, fontSize: 16, fontWeight: 600 }}>New Reservoir</h3>
      <div className="form-row">
        <div className="form-group">
          <label>Reservoir Name</label>
          <input name="reservoir_name" value={form.reservoir_name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Field Name</label>
          <input name="field_name" value={form.field_name} onChange={handleChange} required />
        </div>
      </div>
      <div className="form-row">
        <div className="form-group">
          <label>Reservoir Type</label>
          <select name="reservoir_type" value={form.reservoir_type} onChange={handleChange}>
            <option value="oil">Oil</option>
            <option value="gas">Gas</option>
            <option value="condensate">Condensate</option>
          </select>
        </div>
        <div className="form-group">
          <label>Depth (m)</label>
          <input name="depth_m" type="number" step="0.1" value={form.depth_m} onChange={handleChange} required />
        </div>
      </div>
      <div className="form-row">
        <div className="form-group">
          <label>Porosity (%)</label>
          <input name="porosity_pct" type="number" step="0.1" value={form.porosity_pct} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Permeability (mD)</label>
          <input name="permeability_md" type="number" step="0.1" value={form.permeability_md} onChange={handleChange} required />
        </div>
      </div>
      <div className="form-row">
        <div className="form-group">
          <label>Initial Pressure</label>
          <input name="pressure_initial" type="number" step="0.1" value={form.pressure_initial} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>OOIP (MMBOE)</label>
          <input name="oil_in_place_mmboe" type="number" step="0.1" value={form.oil_in_place_mmboe} onChange={handleChange} required />
        </div>
      </div>
      <div className="form-row">
        <div className="form-group">
          <label>Gas in Place (BCF)</label>
          <input name="gas_in_place_bcf" type="number" step="0.1" value={form.gas_in_place_bcf} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Recovery Factor (%)</label>
          <input name="recovery_factor_pct" type="number" step="0.1" value={form.recovery_factor_pct} onChange={handleChange} required />
        </div>
      </div>
      <button type="submit" className="btn-primary" disabled={saving} style={{ marginTop: 8 }}>
        {saving ? 'Saving...' : 'Add Reservoir'}
      </button>
    </form>
  )
}
