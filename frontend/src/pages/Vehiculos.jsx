import { useState, useEffect } from 'react'
import { vehiculoAPI, modeloAPI } from '../services/api'
import { FaPlus, FaEdit, FaTrash, FaTimes, FaSave } from 'react-icons/fa'
import { validarPatenteArgentina, formatearPatenteInput } from '../utils/patenteValidator'
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
  const [patenteError, setPatenteError] = useState('')
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

  const handlePatenteChange = (e) => {
    const valor = e.target.value
    const patenteFormateada = formatearPatenteInput(valor)
    const validacion = validarPatenteArgentina(patenteFormateada)
    
    setFormData({ ...formData, patente: patenteFormateada })
    
    if (patenteFormateada.length > 0 && !validacion.isValid) {
      setPatenteError(validacion.message)
    } else {
      setPatenteError('')
    }
  }

  const handleCostoChange = (e) => {
    let valor = e.target.value.replace(/[^0-9.,]/g, '')
    // Permitir solo números, punto o coma
    setFormData({ ...formData, costo_diario: valor })
  }

  const formatCostoDisplay = (valor) => {
    if (!valor) return ''
    // Convertir a número (acepta tanto punto como coma como separador decimal)
    const numero = parseFloat(valor.replace(',', '.'))
    if (isNaN(numero)) return valor
    return numero.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
  }

  const parseCostoToNumber = (valor) => {
    if (!valor) return 0
    // Remover puntos de miles y convertir coma a punto
    const limpio = valor.replace(/\./g, '').replace(',', '.')
    return parseFloat(limpio) || 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Validar patente antes de enviar
    const validacionPatente = validarPatenteArgentina(formData.patente)
    if (!validacionPatente.isValid) {
      setPatenteError(validacionPatente.message)
      return
    }

    try {
      const data = {
        ...formData,
        id_modelo: parseInt(formData.id_modelo),
        anio: parseInt(formData.anio),
        patente: validacionPatente.patenteFormateada,
        costo_diario: parseCostoToNumber(formData.costo_diario),
      }
      if (editingId) {
        await vehiculoAPI.actualizar(editingId, data)
      } else {
        await vehiculoAPI.crear(data)
      }
      cargarVehiculos()
      resetForm()
      setPatenteError('')
    } catch (err) {
      setError(err.message)
    }
  }

  const handleEdit = (vehiculo) => {
    try {
      if (!vehiculo || !vehiculo.id) {
        setError('Error: Vehículo inválido')
        return
      }

      setEditingId(vehiculo.id)
      
      // Formatear costo_diario para el input (convertir número a string con formato)
      let costoFormateado = ''
      if (vehiculo.costo_diario !== null && vehiculo.costo_diario !== undefined) {
        const costoNum = typeof vehiculo.costo_diario === 'number' 
          ? vehiculo.costo_diario 
          : parseFloat(vehiculo.costo_diario)
        if (!isNaN(costoNum) && costoNum > 0) {
          // Formatear con coma como separador decimal
          costoFormateado = costoNum.toFixed(2).replace('.', ',')
        }
      }
      
      // Asegurar que modelo existe y tiene id
      const modeloId = (vehiculo.modelo && vehiculo.modelo.id) 
        ? vehiculo.modelo.id.toString() 
        : ''
      
      setFormData({
        id_modelo: modeloId,
        anio: (vehiculo.anio !== null && vehiculo.anio !== undefined) 
          ? vehiculo.anio.toString() 
          : '',
        tipo: vehiculo.tipo || '',
        patente: vehiculo.patente || '',
        costo_diario: costoFormateado,
      })
      setShowForm(true)
      setPatenteError('')
      setError(null) // Limpiar errores previos
    } catch (error) {
      console.error('Error al editar vehículo:', error)
      setError('Error al cargar los datos del vehículo para editar: ' + error.message)
    }
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
    setPatenteError('')
  }

  if (loading) return <div className="loading">Cargando vehículos...</div>

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h2 style={{ margin: 0 }}>Vehículos</h2>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? (
            <>
              <FaTimes style={{ marginRight: '0.5rem' }} />
              Cancelar
            </>
          ) : (
            <>
              <FaPlus style={{ marginRight: '0.5rem' }} />
              Nuevo Vehículo
            </>
          )}
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
              <label>Modelo<span className="required-asterisk"> *</span></label>
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
                <label>Año<span className="required-asterisk"> *</span></label>
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
                <label>Tipo<span className="required-asterisk"> *</span></label>
                <select
                  value={formData.tipo}
                  onChange={(e) => setFormData({ ...formData, tipo: e.target.value })}
                  required
                >
                  <option value="">Seleccione tipo</option>
                  <option value="SEDAN">Sedán</option>
                  <option value="SUV">SUV</option>
                  <option value="HATCHBACK">Hatchback</option>
                  <option value="CAMIONETA">Camioneta</option>
                  <option value="PICKUP">Pickup</option>
                  <option value="COUPE">Coupé</option>
                  <option value="CONVERTIBLE">Convertible</option>
                  <option value="STATION_WAGON">Station Wagon</option>
                  <option value="VAN">Van</option>
                  <option value="MOTOCICLETA">Motocicleta</option>
                </select>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Patente<span className="required-asterisk"> *</span> <span style={{ fontSize: '12px', fontWeight: 'normal', color: 'var(--gray-500)' }}>(Argentina)</span></label>
                <input
                  type="text"
                  value={formData.patente}
                  onChange={handlePatenteChange}
                  required
                  maxLength="7"
                  placeholder="ABC123 o AB123CD"
                  style={{ 
                    borderColor: patenteError ? 'var(--danger)' : undefined,
                    textTransform: 'uppercase'
                  }}
                />
                {patenteError && (
                  <small style={{ color: 'var(--danger)', fontSize: '12px', marginTop: '4px', display: 'block' }}>
                    {patenteError}
                  </small>
                )}
                {formData.patente && !patenteError && (
                  <small style={{ color: 'var(--success)', fontSize: '12px', marginTop: '4px', display: 'block' }}>
                    ✓ Formato válido
                  </small>
                )}
              </div>
              <div className="form-group">
                <label>Costo Diario<span className="required-asterisk"> *</span> <span style={{ fontSize: '12px', fontWeight: 'normal', color: 'var(--gray-500)' }}>(ARS $)</span></label>
                <div style={{ position: 'relative' }}>
                  <span style={{
                    position: 'absolute',
                    left: '12px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    color: 'var(--gray-500)',
                    fontWeight: '500'
                  }}>$</span>
                  <input
                    type="text"
                    value={formData.costo_diario}
                    onChange={handleCostoChange}
                    required
                    placeholder="0,00"
                    style={{ paddingLeft: '32px' }}
                  />
                </div>
                {formData.costo_diario && (
                  <small style={{ color: 'var(--gray-500)', fontSize: '12px', marginTop: '4px', display: 'block' }}>
                    {formatCostoDisplay(formData.costo_diario)} ARS
                  </small>
                )}
              </div>
            </div>

            <div className="form-actions">
              <button type="button" className="btn btn-secondary" onClick={resetForm}>
                <FaTimes style={{ marginRight: '0.5rem' }} />
                Cancelar
              </button>
              <button type="submit" className="btn btn-primary" disabled={!!patenteError}>
                {editingId ? (
                  <>
                    <FaSave style={{ marginRight: '0.5rem' }} />
                    Actualizar
                  </>
                ) : (
                  <>
                    <FaPlus style={{ marginRight: '0.5rem' }} />
                    Crear
                  </>
                )}
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
              {vehiculos.map((vehiculo) => {
                if (!vehiculo || !vehiculo.id) return null
                
                const modeloNombre = vehiculo.modelo 
                  ? `${vehiculo.modelo.marca?.nombre || ''} ${vehiculo.modelo.nombre || ''}`.trim()
                  : 'Sin modelo'
                
                const costoDiario = vehiculo.costo_diario !== null && vehiculo.costo_diario !== undefined
                  ? vehiculo.costo_diario
                  : 0
                
                return (
                  <tr key={vehiculo.id}>
                    <td>{vehiculo.id}</td>
                    <td>{vehiculo.patente || '-'}</td>
                    <td>{modeloNombre}</td>
                    <td>{vehiculo.anio || '-'}</td>
                    <td>{vehiculo.tipo || '-'}</td>
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
                        {vehiculo.estado || '-'}
                      </span>
                    </td>
                    <td>
                      <strong style={{ color: 'var(--brand-primary)' }}>
                        ${typeof costoDiario === 'number' 
                          ? costoDiario.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
                          : '0,00'} ARS
                      </strong>
                    </td>
                    <td>
                      <div className="actions">
                        <button
                          className="btn btn-secondary btn-small"
                          onClick={() => {
                            try {
                              handleEdit(vehiculo)
                            } catch (err) {
                              console.error('Error al hacer clic en editar:', err)
                              setError('Error al abrir el formulario de edición')
                            }
                          }}
                          title="Editar vehículo"
                        >
                          <FaEdit style={{ marginRight: '0.3rem' }} />
                          Editar
                        </button>
                        <button
                          className="btn btn-danger btn-small"
                          onClick={() => {
                            try {
                              handleDelete(vehiculo.id)
                            } catch (err) {
                              console.error('Error al eliminar:', err)
                              setError('Error al eliminar el vehículo')
                            }
                          }}
                          title="Eliminar vehículo"
                        >
                          <FaTrash style={{ marginRight: '0.3rem' }} />
                          Eliminar
                        </button>
                      </div>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default Vehiculos

