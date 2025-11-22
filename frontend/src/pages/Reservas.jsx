import { useState, useEffect } from 'react'
import { reservaAPI, clienteAPI, vehiculoAPI } from '../services/api'
import '../components/Table.css'
import '../components/Form.css'

function Reservas() {
  const [reservas, setReservas] = useState([])
  const [clientes, setClientes] = useState([])
  const [vehiculos, setVehiculos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [formData, setFormData] = useState({
    id_cliente: '',
    id_vehiculo: '',
    fecha_inicio: '',
    fecha_fin: '',
  })

  useEffect(() => {
    cargarReservas()
    cargarClientes()
    cargarVehiculos()
  }, [])

  const cargarReservas = async () => {
    try {
      setLoading(true)
      const data = await reservaAPI.listar()
      setReservas(data)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const cargarClientes = async () => {
    try {
      const data = await clienteAPI.listar()
      setClientes(data)
    } catch (err) {
      console.error('Error cargando clientes:', err)
    }
  }

  const cargarVehiculos = async () => {
    try {
      const data = await vehiculoAPI.listar()
      setVehiculos(data)
    } catch (err) {
      console.error('Error cargando vehículos:', err)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = {
        id_cliente: parseInt(formData.id_cliente),
        id_vehiculo: parseInt(formData.id_vehiculo),
        fecha_inicio: formData.fecha_inicio,
        fecha_fin: formData.fecha_fin,
      }
      if (editingId) {
        await reservaAPI.actualizar(editingId, data)
      } else {
        await reservaAPI.crear(data)
      }
      cargarReservas()
      resetForm()
    } catch (err) {
      setError(err.message)
    }
  }

  const handleEdit = (reserva) => {
    setEditingId(reserva.id)
    setFormData({
      id_cliente: reserva.cliente?.id || '',
      id_vehiculo: reserva.vehiculo?.id || '',
      fecha_inicio: reserva.fecha_inicio || '',
      fecha_fin: reserva.fecha_fin || '',
    })
    setShowForm(true)
  }

  const handleCancelar = async (id) => {
    if (window.confirm('¿Está seguro de cancelar esta reserva?')) {
      try {
        await reservaAPI.cancelar(id)
        cargarReservas()
      } catch (err) {
        setError(err.message)
      }
    }
  }

  const resetForm = () => {
    setFormData({
      id_cliente: '',
      id_vehiculo: '',
      fecha_inicio: '',
      fecha_fin: '',
    })
    setEditingId(null)
    setShowForm(false)
  }

  if (loading) return <div className="loading">Cargando reservas...</div>

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2>Reservas</h2>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Nueva Reserva'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {showForm && (
        <div className="form-container" style={{ marginBottom: '2rem' }}>
          <h3>{editingId ? 'Editar Reserva' : 'Nueva Reserva'}</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Cliente *</label>
              <select
                value={formData.id_cliente}
                onChange={(e) => setFormData({ ...formData, id_cliente: e.target.value })}
                required
              >
                <option value="">Seleccione un cliente</option>
                {clientes.map((cliente) => (
                  <option key={cliente.id} value={cliente.id}>
                    {cliente.nombre} {cliente.apellido} - DNI: {cliente.dni}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Vehículo *</label>
              <select
                value={formData.id_vehiculo}
                onChange={(e) => setFormData({ ...formData, id_vehiculo: e.target.value })}
                required
              >
                <option value="">Seleccione un vehículo</option>
                {vehiculos.map((vehiculo) => (
                  <option key={vehiculo.id} value={vehiculo.id}>
                    {vehiculo.patente} - {vehiculo.modelo?.marca?.nombre} {vehiculo.modelo?.nombre}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Fecha Inicio *</label>
                <input
                  type="date"
                  value={formData.fecha_inicio}
                  onChange={(e) => setFormData({ ...formData, fecha_inicio: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>Fecha Fin *</label>
                <input
                  type="date"
                  value={formData.fecha_fin}
                  onChange={(e) => setFormData({ ...formData, fecha_fin: e.target.value })}
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
        {reservas.length === 0 ? (
          <div className="empty-state">
            <p>No hay reservas registradas</p>
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Cliente</th>
                <th>Vehículo</th>
                <th>Fecha Inicio</th>
                <th>Fecha Fin</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {reservas.map((reserva) => (
                <tr key={reserva.id}>
                  <td>{reserva.id}</td>
                  <td>{reserva.cliente?.nombre} {reserva.cliente?.apellido}</td>
                  <td>{reserva.vehiculo?.patente}</td>
                  <td>{reserva.fecha_inicio}</td>
                  <td>{reserva.fecha_fin}</td>
                  <td>
                    <span style={{
                      padding: '0.3rem 0.6rem',
                      borderRadius: '4px',
                      fontSize: '0.85rem',
                      backgroundColor: reserva.estado === 'PENDIENTE' ? '#fff3cd' : 
                                      reserva.estado === 'CONFIRMADA' ? '#d4edda' : '#f8d7da',
                      color: reserva.estado === 'PENDIENTE' ? '#856404' : 
                            reserva.estado === 'CONFIRMADA' ? '#155724' : '#721c24'
                    }}>
                      {reserva.estado}
                    </span>
                  </td>
                  <td>
                    <div className="actions">
                      {reserva.estado !== 'CANCELADA' && (
                        <button
                          className="btn btn-warning btn-small"
                          onClick={() => handleCancelar(reserva.id)}
                        >
                          Cancelar
                        </button>
                      )}
                      <button
                        className="btn btn-secondary btn-small"
                        onClick={() => handleEdit(reserva)}
                      >
                        Editar
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

export default Reservas

