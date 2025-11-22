import { useState, useEffect } from 'react'
import { modeloAPI, marcaAPI } from '../services/api'
import '../components/Table.css'
import '../components/Form.css'

function Modelos() {
  const [modelos, setModelos] = useState([])
  const [marcas, setMarcas] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [formData, setFormData] = useState({
    id_marca: '',
    nombre: '',
    descripcion: '',
  })

  useEffect(() => {
    cargarModelos()
    cargarMarcas()
  }, [])

  const cargarModelos = async () => {
    try {
      setLoading(true)
      const data = await modeloAPI.listar()
      setModelos(data)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const cargarMarcas = async () => {
    try {
      const data = await marcaAPI.listar()
      setMarcas(data)
    } catch (err) {
      console.error('Error cargando marcas:', err)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = {
        ...formData,
        id_marca: parseInt(formData.id_marca),
      }
      if (editingId) {
        await modeloAPI.actualizar(editingId, data)
      } else {
        await modeloAPI.crear(data)
      }
      cargarModelos()
      resetForm()
    } catch (err) {
      setError(err.message)
    }
  }

  const handleEdit = (modelo) => {
    setEditingId(modelo.id)
    setFormData({
      id_marca: modelo.marca?.id || '',
      nombre: modelo.nombre || '',
      descripcion: modelo.descripcion || '',
    })
    setShowForm(true)
  }

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este modelo?')) {
      try {
        await modeloAPI.eliminar(id)
        cargarModelos()
      } catch (err) {
        setError(err.message)
      }
    }
  }

  const resetForm = () => {
    setFormData({
      id_marca: '',
      nombre: '',
      descripcion: '',
    })
    setEditingId(null)
    setShowForm(false)
  }

  if (loading) return <div className="loading">Cargando modelos...</div>

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2>Modelos</h2>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Nuevo Modelo'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {showForm && (
        <div className="form-container" style={{ marginBottom: '2rem' }}>
          <h3>{editingId ? 'Editar Modelo' : 'Nuevo Modelo'}</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Marca *</label>
              <select
                value={formData.id_marca}
                onChange={(e) => setFormData({ ...formData, id_marca: e.target.value })}
                required
              >
                <option value="">Seleccione una marca</option>
                {marcas.map((marca) => (
                  <option key={marca.id} value={marca.id}>
                    {marca.nombre}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Nombre *</label>
              <input
                type="text"
                value={formData.nombre}
                onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                required
              />
            </div>

            <div className="form-group">
              <label>Descripción *</label>
              <textarea
                value={formData.descripcion}
                onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })}
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
        {modelos.length === 0 ? (
          <div className="empty-state">
            <p>No hay modelos registrados</p>
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Marca</th>
                <th>Nombre</th>
                <th>Descripción</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {modelos.map((modelo) => (
                <tr key={modelo.id}>
                  <td>{modelo.id}</td>
                  <td>{modelo.marca?.nombre}</td>
                  <td>{modelo.nombre}</td>
                  <td>{modelo.descripcion}</td>
                  <td>
                    <div className="actions">
                      <button
                        className="btn btn-secondary btn-small"
                        onClick={() => handleEdit(modelo)}
                      >
                        Editar
                      </button>
                      <button
                        className="btn btn-danger btn-small"
                        onClick={() => handleDelete(modelo.id)}
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

export default Modelos

