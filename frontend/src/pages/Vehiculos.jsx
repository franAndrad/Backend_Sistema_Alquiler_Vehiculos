import { useState, useEffect } from 'react'
import { vehiculoAPI, modeloAPI } from '../services/api'
import '../components/Table.css'
import '../components/Form.css'

function Vehiculos() {
  const [vehiculos, setVehiculos] = useState([])
  const [modelos, setModelos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [filtroEstado, setFiltroEstado] = useState('')
  const [formData, setFormData] = useState({
    id_modelo: '',
    anio: '',
    tipo: '',
    patente: '',
    costo_diario: '',
  })

  useEffect(() => {
    cargarVehiculos()
    cargarModelos()
  }, [])

  useEffect(() => {
    if (filtroEstado) {
      cargarVehiculosPorEstado()
    } else {
      cargarVehiculos()
    }
  }, [filtroEstado])

  const cargarVehiculos = async () => {
    try {
      setLoading(true)
      const data = await vehiculoAPI.listar()
      setVehiculos(data)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const cargarVehiculosPorEstado = async () => {
    try {
      setLoading(true)
      const data = await vehiculoAPI.obtenerPorEstado(filtroEstado)
      setVehiculos(data)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const cargarModelos = async () => {
    try {
      const data = await modeloAPI.listar()
      setModelos(data)
    } catch (err) {
      console.error('Error cargando modelos:', err)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = {
        ...formData,
        id_modelo: parseInt(formData.id_modelo),
        anio: parseInt(formData.anio),
        costo_diario: parseFloat(formData.costo_diario),
      }
      if (editingId) {
        await vehiculoAPI.actualizar(editingId, data)
      } else {
        await vehiculoAPI.crear(data)
      }
      cargarVehiculos()
      resetForm()
    } catch (err) {
      setError(err.message)
    }
  }

  const handleEdit = (vehiculo) => {
    setEditingId(vehiculo.id)
    setFormData({
      id_modelo: vehiculo.modelo?.id || '',
      anio: vehiculo.anio || '',
      tipo: vehiculo.tipo || '',
      patente: vehiculo.patente || '',
      costo_diario: vehiculo.costo_diario || '',
    })
    setShowForm(true)
  }

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este vehículo?')) {
      try {
        await vehiculoAPI.eliminar(id)
        cargarVehiculos()
      } catch (err) {
        setError(err.message)
      }
    }
  }

  const resetForm = () => {
    setFormData({
      id_modelo: '',
      anio: '',
      tipo: '',
      patente: '',
      costo_diario: '',
    })
    setEditingId(null)
    setShowForm(false)
  }

  if (loading) return <div className="loading">Cargando vehículos...</div>

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2>Vehículos</h2>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Nuevo Vehículo'}
        </button>
      </div>

      <div style={{ marginBottom: '1rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <label>Filtrar por estado:</label>
        <select
          value={filtroEstado}
          onChange={(e) => setFiltroEstado(e.target.value)}
          style={{ padding: '0.5rem', borderRadius: '6px', border: '1px solid #ced4da' }}
        >
          <option value="">Todos</option>
          <option value="DISPONIBLE">Disponible</option>
          <option value="ALQUILADO">Alquilado</option>
          <option value="EN_MANTENIMIENTO">En Mantenimiento</option>
        </select>
      </div>

      {error && <div className="error">{error}</div>}

      {showForm && (
        <div className="form-container" style={{ marginBottom: '2rem' }}>
          <h3>{editingId ? 'Editar Vehículo' : 'Nuevo Vehículo'}</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Modelo *</label>
              <select
                value={formData.id_modelo}
                onChange={(e) => setFormData({ ...formData, id_modelo: e.target.value })}
                required
              >
                <option value="">Seleccione un modelo</option>
                {modelos.map((modelo) => (
                  <option key={modelo.id} value={modelo.id}>
                    {modelo.marca?.nombre} - {modelo.nombre}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Año *</label>
                <input
                  type="number"
                  value={formData.anio}
                  onChange={(e) => setFormData({ ...formData, anio: e.target.value })}
                  required
                  min="1900"
                  max="2100"
                />
              </div>
              <div className="form-group">
                <label>Tipo *</label>
                <select
                  value={formData.tipo}
                  onChange={(e) => setFormData({ ...formData, tipo: e.target.value })}
                  required
                >
                  <option value="">Seleccione tipo</option>
                  <option value="SEDAN">Sedan</option>
                  <option value="SUV">SUV</option>
                  <option value="HATCHBACK">Hatchback</option>
                  <option value="PICKUP">Pickup</option>
                  <option value="COUPE">Coupé</option>
                </select>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Patente *</label>
                <input
                  type="text"
                  value={formData.patente}
                  onChange={(e) => setFormData({ ...formData, patente: e.target.value.toUpperCase() })}
                  required
                  maxLength="10"
                />
              </div>
              <div className="form-group">
                <label>Costo Diario *</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.costo_diario}
                  onChange={(e) => setFormData({ ...formData, costo_diario: e.target.value })}
                  required
                  min="0"
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
        {vehiculos.length === 0 ? (
          <div className="empty-state">
            <p>No hay vehículos registrados</p>
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Patente</th>
                <th>Modelo</th>
                <th>Año</th>
                <th>Tipo</th>
                <th>Estado</th>
                <th>Costo Diario</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {vehiculos.map((vehiculo) => (
                <tr key={vehiculo.id}>
                  <td>{vehiculo.id}</td>
                  <td>{vehiculo.patente}</td>
                  <td>{vehiculo.modelo?.marca?.nombre} {vehiculo.modelo?.nombre}</td>
                  <td>{vehiculo.anio}</td>
                  <td>{vehiculo.tipo}</td>
                  <td>
                    <span style={{
                      padding: '0.3rem 0.6rem',
                      borderRadius: '4px',
                      fontSize: '0.85rem',
                      backgroundColor: vehiculo.estado === 'DISPONIBLE' ? '#d4edda' : 
                                      vehiculo.estado === 'ALQUILADO' ? '#fff3cd' : '#f8d7da',
                      color: vehiculo.estado === 'DISPONIBLE' ? '#155724' : 
                            vehiculo.estado === 'ALQUILADO' ? '#856404' : '#721c24'
                    }}>
                      {vehiculo.estado}
                    </span>
                  </td>
                  <td>${vehiculo.costo_diario?.toLocaleString()}</td>
                  <td>
                    <div className="actions">
                      <button
                        className="btn btn-secondary btn-small"
                        onClick={() => handleEdit(vehiculo)}
                      >
                        Editar
                      </button>
                      <button
                        className="btn btn-danger btn-small"
                        onClick={() => handleDelete(vehiculo.id)}
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

export default Vehiculos

