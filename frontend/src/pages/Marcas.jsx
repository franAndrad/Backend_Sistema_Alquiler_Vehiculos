import { useState, useEffect } from 'react'
import { marcaAPI } from '../services/api'
import '../components/Table.css'
import '../components/Form.css'

function Marcas() {
  const [marcas, setMarcas] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [formData, setFormData] = useState({
    nombre: '',
  })

  useEffect(() => {
    cargarMarcas()
  }, [])

  const cargarMarcas = async () => {
    try {
      setLoading(true)
      const data = await marcaAPI.listar()
      setMarcas(data)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingId) {
        await marcaAPI.actualizar(editingId, formData)
      } else {
        await marcaAPI.crear(formData)
      }
      cargarMarcas()
      resetForm()
    } catch (err) {
      setError(err.message)
    }
  }

  const handleEdit = (marca) => {
    setEditingId(marca.id)
    setFormData({
      nombre: marca.nombre || '',
    })
    setShowForm(true)
  }

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar esta marca?')) {
      try {
        await marcaAPI.eliminar(id)
        cargarMarcas()
      } catch (err) {
        setError(err.message)
      }
    }
  }

  const resetForm = () => {
    setFormData({
      nombre: '',
    })
    setEditingId(null)
    setShowForm(false)
  }

  if (loading) return <div className="loading">Cargando marcas...</div>

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2>Marcas</h2>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Nueva Marca'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {showForm && (
        <div className="form-container" style={{ marginBottom: '2rem' }}>
          <h3>{editingId ? 'Editar Marca' : 'Nueva Marca'}</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Nombre *</label>
              <input
                type="text"
                value={formData.nombre}
                onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                required
              />
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
        {marcas.length === 0 ? (
          <div className="empty-state">
            <p>No hay marcas registradas</p>
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {marcas.map((marca) => (
                <tr key={marca.id}>
                  <td>{marca.id}</td>
                  <td>{marca.nombre}</td>
                  <td>
                    <div className="actions">
                      <button
                        className="btn btn-secondary btn-small"
                        onClick={() => handleEdit(marca)}
                      >
                        Editar
                      </button>
                      <button
                        className="btn btn-danger btn-small"
                        onClick={() => handleDelete(marca.id)}
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

export default Marcas

