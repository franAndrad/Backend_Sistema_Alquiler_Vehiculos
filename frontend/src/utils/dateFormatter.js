/**
 * Formatea una fecha para mostrar solo la fecha (YYYY-MM-DD) sin hora ni zona horaria
 * @param {string|Date} fecha - La fecha a formatear
 * @param {boolean} mostrarGuion - Si es true, muestra '-' cuando no hay fecha
 * @returns {string} - Fecha formateada como YYYY-MM-DD
 */
export const formatearFecha = (fecha, mostrarGuion = false) => {
  if (!fecha) return mostrarGuion ? '-' : ''
  
  // Si es string, procesarlo directamente
  if (typeof fecha === 'string') {
    const fechaString = fecha.trim()
    
    // Extraer solo la parte de fecha usando regex (más robusto)
    const match = fechaString.match(/^(\d{4}-\d{2}-\d{2})/)
    if (match) {
      return match[1]
    }
    
    // Si ya es solo fecha (YYYY-MM-DD), retornarla tal cual
    if (/^\d{4}-\d{2}-\d{2}$/.test(fechaString)) {
      return fechaString
    }
  }
  
  // Si es un objeto Date o se puede convertir
  try {
    const fechaObj = fecha instanceof Date ? fecha : new Date(fecha)
    
    if (isNaN(fechaObj.getTime())) {
      return mostrarGuion ? '-' : ''
    }
    
    // Usar métodos locales para evitar problemas de zona horaria
    const year = fechaObj.getFullYear()
    const month = String(fechaObj.getMonth() + 1).padStart(2, '0')
    const day = String(fechaObj.getDate()).padStart(2, '0')
    
    return `${year}-${month}-${day}`
  } catch (e) {
    return mostrarGuion ? '-' : ''
  }
}

/**
 * Formatea una fecha en formato legible (DD/MM/YYYY)
 * @param {string|Date} fecha - La fecha a formatear
 * @returns {string} - Fecha formateada como DD/MM/YYYY
 */
export const formatearFechaLegible = (fecha) => {
  const fechaFormateada = formatearFecha(fecha)
  if (!fechaFormateada || fechaFormateada === '-') return '-'
  
  const [year, month, day] = fechaFormateada.split('-')
  return `${day}/${month}/${year}`
}

