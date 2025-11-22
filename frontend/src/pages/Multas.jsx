import { useState, useEffect } from 'react'
import { multaAPI, alquilerAPI } from '../services/api'
import '../components/Table.css'
import '../components/Form.css'

function Multas() {
  const [multas, setMultas] = useState([])
  const [alquileres, setAlquileres] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [formData, setFormData] = useState({
    id_alquiler: '',
    descripcion: '',
    monto: '',
    fecha: '',
  })

  useEffect(() => {
    cargarMultas()
    cargarAlquileres()
  }, [])

  const cargarMultas = async () => {
    try {
      setLoading(true)
      const data = await multaAPI.listar()
      setMultas(data)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const cargarAlquileres = async () => {
    try {
      const data = await alquilerAPI.listar()
      setAlquileres(data)
    } catch (err) {
      console.error('Error cargando alquileres:', err)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = {
        id_alquiler: parseInt(formData.id_alquiler),
        descripcion: formData.descripcion,
        monto: parseFloat(formData.monto),
        fecha: formData.fecha,
      }
      if (editingId) {
        await multaAPI.actualizar(editingId, data)
      } else {
        await multaAPI.crear(data)
      }
      cargarMultas()
      resetForm()
    } catch (err) {
      setError(err.message)
    }
  }

  const handleEdit = (multa) => {
    setEditingId(multa.id)
    setFormData({
      id_alquiler: multa.id_alquiler || '',
      descripcion: multa.descripcion || '',
      monto: multa.monto || '',
      fecha: multa.fecha || '',
    })
    setShowForm(true)
  }

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar esta multa?')) {
      try {
        await multaAPI.eliminar(id)
        cargarMultas()
      } catch (err) {
        setError(err.message)
      }
    }
  }

  const resetForm = () => {
    setFormData({
      id_alquiler: '',
      descripcion: '',
      monto: '',
      fecha: '',
    })
    setEditingId(null)
    setShowForm(false)
  }

  if (loading) return <div className="loading">Cargando multas...</div>

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2>Multas</h2>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Nueva Multa'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {showForm && (
        <div className="form-container" style={{ marginBottom: '2rem' }}>
          <h3>{editingId ? 'Editar Multa' : 'Nueva Multa'}</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Alquiler *</label>
              <select
                value={formData.id_alquiler}
                onChange={(e) => setFormData({ ...formData, id_alquiler: e.target.value })}
                required
              >
                <option value="">Seleccione un alquiler</option>
                {alquileres.map((alquiler) => (
                  <option key={alquiler.id} value={alquiler.id}>
                    ID: {alquiler.id} - Cliente: {alquiler.cliente?.nombre} {alquiler.cliente?.apellido} - Vehículo: {alquiler.vehiculo?.patente}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Descripción *</label>
              <textarea
                value={formData.descripcion}
                onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Monto *</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.monto}
                  onChange={(e) => setFormData({ ...formData, monto: e.target.value })}
                  required
                  min="0"
                />
              </div>
              <div className="form-group">
                <label>Fecha *</label>
                <input
                  type="date"
                  value={formData.fecha}
                  onChange={(e) => setFormData({ ...formData, fecha: e.target.value })}
                  required
                />
              </div>
            </div>

            <div className="form-actions">
              <button type="button" className="btn btn-secondary" onClick={resetForm}>
                Cancelar
              </button>
              <button type="submit" className="btn btn-primary">
                {editingId ? 'Actualizar' : 'Crear'}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="table-container">
        {multas.length === 0 ? (
          <div className="empty-state">
            <p>No hay multas registradas</p>
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>ID Alquiler</th>
                <th>Descripción</th>
                <th>Monto</th>
                <th>Fecha</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {multas.map((multa) => (
                <tr key={multa.id}>
                  <td>{multa.id}</td>
                  <td>{multa.id_alquiler}</td>
                  <td>{multa.descripcion}</td>
                  <td>${multa.monto?.toLocaleString()}</td>
                  <td>{multa.fecha}</td>
                  <td>
                    <div className="actions">
                      <button
                        className="btn btn-secondary btn-small"
                        onClick={() => handleEdit(multa)}
                      >
                        Editar
                      </button>
                      <button
                        className="btn btn-danger btn-small"
                        onClick={() => handleDelete(multa.id)}
                      >
                        Eliminar
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default Multas

