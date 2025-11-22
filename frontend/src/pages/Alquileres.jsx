import { useState, useEffect } from 'react'
import { alquilerAPI, clienteAPI, vehiculoAPI, empleadoAPI } from '../services/api'
import '../components/Table.css'
import '../components/Form.css'

function Alquileres() {
  const [alquileres, setAlquileres] = useState([])
  const [clientes, setClientes] = useState([])
  const [vehiculos, setVehiculos] = useState([])
  const [empleados, setEmpleados] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [formData, setFormData] = useState({
    id_cliente: '',
    id_vehiculo: '',
    id_empleado: '',
    fecha_inicio: '',
    fecha_fin: '',
  })

  useEffect(() => {
    cargarAlquileres()
    cargarClientes()
    cargarVehiculos()
    cargarEmpleados()
  }, [])

  const cargarAlquileres = async () => {
    try {
      setLoading(true)
      const data = await alquilerAPI.listar()
      setAlquileres(data)
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

  const cargarEmpleados = async () => {
    try {
      const data = await empleadoAPI.listar()
      setEmpleados(data)
    } catch (err) {
      console.error('Error cargando empleados:', err)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = {
        id_cliente: parseInt(formData.id_cliente),
        id_vehiculo: parseInt(formData.id_vehiculo),
        id_empleado: parseInt(formData.id_empleado),
        fecha_inicio: formData.fecha_inicio,
        fecha_fin: formData.fecha_fin || null,
      }
      if (editingId) {
        await alquilerAPI.actualizar(editingId, data)
      } else {
        await alquilerAPI.crear(data)
      }
      cargarAlquileres()
      cargarVehiculos()
      resetForm()
    } catch (err) {
      setError(err.message)
    }
  }

  const handleEdit = (alquiler) => {
    setEditingId(alquiler.id)
    setFormData({
      id_cliente: alquiler.cliente?.id || '',
      id_vehiculo: alquiler.vehiculo?.id || '',
      id_empleado: alquiler.empleado?.id || '',
      fecha_inicio: alquiler.fecha_inicio || '',
      fecha_fin: alquiler.fecha_fin || '',
    })
    setShowForm(true)
  }

  const handleFinalizar = async (id) => {
    if (window.confirm('¿Está seguro de finalizar este alquiler?')) {
      try {
        await alquilerAPI.finalizar(id)
        cargarAlquileres()
        cargarVehiculos()
      } catch (err) {
        setError(err.message)
      }
    }
  }

  const resetForm = () => {
    setFormData({
      id_cliente: '',
      id_vehiculo: '',
      id_empleado: '',
      fecha_inicio: '',
      fecha_fin: '',
    })
    setEditingId(null)
    setShowForm(false)
  }

  if (loading) return <div className="loading">Cargando alquileres...</div>

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2>Alquileres</h2>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Nuevo Alquiler'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {showForm && (
        <div className="form-container" style={{ marginBottom: '2rem' }}>
          <h3>{editingId ? 'Editar Alquiler' : 'Nuevo Alquiler'}</h3>
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

            <div className="form-group">
              <label>Empleado *</label>
              <select
                value={formData.id_empleado}
                onChange={(e) => setFormData({ ...formData, id_empleado: e.target.value })}
                required
              >
                <option value="">Seleccione un empleado</option>
                {empleados.map((empleado) => (
                  <option key={empleado.id} value={empleado.id}>
                    {empleado.nombre} {empleado.apellido} - {empleado.rol}
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
                <label>Fecha Fin</label>
                <input
                  type="date"
                  value={formData.fecha_fin}
                  onChange={(e) => setFormData({ ...formData, fecha_fin: e.target.value })}
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
        {alquileres.length === 0 ? (
          <div className="empty-state">
            <p>No hay alquileres registrados</p>
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Cliente</th>
                <th>Vehículo</th>
                <th>Empleado</th>
                <th>Fecha Inicio</th>
                <th>Fecha Fin</th>
                <th>Costo Total</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {alquileres.map((alquiler) => (
                <tr key={alquiler.id}>
                  <td>{alquiler.id}</td>
                  <td>{alquiler.cliente?.nombre} {alquiler.cliente?.apellido}</td>
                  <td>{alquiler.vehiculo?.patente}</td>
                  <td>{alquiler.empleado?.nombre} {alquiler.empleado?.apellido}</td>
                  <td>{alquiler.fecha_inicio}</td>
                  <td>{alquiler.fecha_fin || '-'}</td>
                  <td>{alquiler.costo_total ? `$${alquiler.costo_total.toLocaleString()}` : '-'}</td>
                  <td>
                    <span style={{
                      padding: '0.3rem 0.6rem',
                      borderRadius: '4px',
                      fontSize: '0.85rem',
                      backgroundColor: alquiler.estado === 'ACTIVO' ? '#d4edda' : '#f8d7da',
                      color: alquiler.estado === 'ACTIVO' ? '#155724' : '#721c24'
                    }}>
                      {alquiler.estado}
                    </span>
                  </td>
                  <td>
                    <div className="actions">
                      {alquiler.estado === 'ACTIVO' && (
                        <button
                          className="btn btn-success btn-small"
                          onClick={() => handleFinalizar(alquiler.id)}
                        >
                          Finalizar
                        </button>
                      )}
                      <button
                        className="btn btn-secondary btn-small"
                        onClick={() => handleEdit(alquiler)}
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

export default Alquileres

