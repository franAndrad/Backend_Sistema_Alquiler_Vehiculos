const API_BASE_URL = 'http://localhost:5000'

async function fetchAPI(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  }

  if (config.body && typeof config.body === 'object') {
    config.body = JSON.stringify(config.body)
  }

  try {
    const response = await fetch(url, config)
    const data = await response.json()
    
    if (!response.ok) {
      throw new Error(data.error || `Error: ${response.status}`)
    }
    
    return data
  } catch (error) {
    console.error('API Error:', error)
    throw error
  }
}

export const clienteAPI = {
  listar: () => fetchAPI('/clientes'),
  obtener: (id) => fetchAPI(`/clientes/${id}`),
  crear: (data) => fetchAPI('/clientes', { method: 'POST', body: data }),
  actualizar: (id, data) => fetchAPI(`/clientes/${id}`, { method: 'PUT', body: data }),
  eliminar: (id) => fetchAPI(`/clientes/${id}`, { method: 'DELETE' }),
  obtenerPorDni: (dni) => fetchAPI(`/clientes/dni/${dni}`),
  obtenerPorEmail: (email) => fetchAPI(`/clientes/email/${email}`),
}

export const vehiculoAPI = {
  listar: () => fetchAPI('/vehiculos'),
  obtener: (id) => fetchAPI(`/vehiculos/${id}`),
  crear: (data) => fetchAPI('/vehiculos', { method: 'POST', body: data }),
  actualizar: (id, data) => fetchAPI(`/vehiculos/${id}`, { method: 'PUT', body: data }),
  eliminar: (id) => fetchAPI(`/vehiculos/${id}`, { method: 'DELETE' }),
  obtenerPorEstado: (estados) => fetchAPI(`/vehiculos/estado/${estados}`),
}

export const alquilerAPI = {
  listar: () => fetchAPI('/alquileres'),
  obtener: (id) => fetchAPI(`/alquileres/${id}`),
  crear: (data) => fetchAPI('/alquileres', { method: 'POST', body: data }),
  actualizar: (id, data) => fetchAPI(`/alquileres/${id}`, { method: 'PUT', body: data }),
  finalizar: (id) => fetchAPI(`/alquileres/${id}/finalizar`, { method: 'PATCH' }),
  listarPorCliente: (clienteId) => fetchAPI(`/alquileres/cliente/${clienteId}`),
  listarPorVehiculo: (vehiculoId) => fetchAPI(`/alquileres/vehiculo/${vehiculoId}`),
  listarPorEstado: (estados) => fetchAPI(`/alquileres/estado/${estados}`),
  listarPorPeriodo: (desde, hasta) => fetchAPI(`/alquileres/periodo?desde=${desde}&hasta=${hasta}`),
  vehiculosMasAlquilados: (desde, hasta, limit) => {
    let url = '/alquileres/vehiculos-mas-alquilados?'
    if (desde) url += `desde=${desde}&`
    if (hasta) url += `hasta=${hasta}&`
    if (limit) url += `limit=${limit}`
    return fetchAPI(url)
  },
}

export const reservaAPI = {
  listar: () => fetchAPI('/reservas'),
  obtener: (id) => fetchAPI(`/reservas/${id}`),
  crear: (data) => fetchAPI('/reservas', { method: 'POST', body: data }),
  actualizar: (id, data) => fetchAPI(`/reservas/${id}`, { method: 'PUT', body: data }),
  cancelar: (id) => fetchAPI(`/reservas/${id}/cancelar`, { method: 'PATCH' }),
  listarPorCliente: (clienteId) => fetchAPI(`/reservas/cliente/${clienteId}`),
  listarPorEstado: (estados) => fetchAPI(`/reservas/estado/${estados}`),
}

export const empleadoAPI = {
  listar: () => fetchAPI('/empleados'),
  obtener: (id) => fetchAPI(`/empleados/${id}`),
  crear: (data) => fetchAPI('/empleados', { method: 'POST', body: data }),
  actualizar: (id, data) => fetchAPI(`/empleados/${id}`, { method: 'PUT', body: data }),
  eliminar: (id) => fetchAPI(`/empleados/${id}`, { method: 'DELETE' }),
  listarPorRol: (rol) => fetchAPI(`/empleados/rol/${rol}`),
  obtenerPorDni: (dni) => fetchAPI(`/empleados/dni/${dni}`),
  obtenerPorEmail: (email) => fetchAPI(`/empleados/email/${email}`),
}

export const marcaAPI = {
  listar: () => fetchAPI('/marcas'),
  obtener: (id) => fetchAPI(`/marcas/${id}`),
  crear: (data) => fetchAPI('/marcas', { method: 'POST', body: data }),
  actualizar: (id, data) => fetchAPI(`/marcas/${id}`, { method: 'PUT', body: data }),
  eliminar: (id) => fetchAPI(`/marcas/${id}`, { method: 'DELETE' }),
  obtenerPorNombre: (nombre) => fetchAPI(`/marcas/nombre/${nombre}`),
}

export const modeloAPI = {
  listar: () => fetchAPI('/modelos'),
  obtener: (id) => fetchAPI(`/modelos/${id}`),
  crear: (data) => fetchAPI('/modelos', { method: 'POST', body: data }),
  actualizar: (id, data) => fetchAPI(`/modelos/${id}`, { method: 'PUT', body: data }),
  eliminar: (id) => fetchAPI(`/modelos/${id}`, { method: 'DELETE' }),
}

export const multaAPI = {
  listar: () => fetchAPI('/multas'),
  obtener: (id) => fetchAPI(`/multas/${id}`),
  crear: (data) => fetchAPI('/multas', { method: 'POST', body: data }),
  actualizar: (id, data) => fetchAPI(`/multas/${id}`, { method: 'PUT', body: data }),
  eliminar: (id) => fetchAPI(`/multas/${id}`, { method: 'DELETE' }),
}

