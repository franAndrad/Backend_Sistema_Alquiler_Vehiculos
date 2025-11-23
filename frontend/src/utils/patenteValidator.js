/**
 * Valida el formato de patente argentina
 * Formatos válidos:
 * - Formato antiguo: 3 letras + 3 números (ej: ABC123)
 * - Formato nuevo: 2 letras + 3 números + 2 letras (ej: AB123CD)
 * @param {string} patente - La patente a validar
 * @returns {object} - { isValid: boolean, format: string, message: string }
 */
export const validarPatenteArgentina = (patente) => {
  if (!patente) {
    return { isValid: false, format: null, message: 'La patente es requerida' }
  }

  // Limpiar espacios y convertir a mayúsculas
  const patenteLimpia = patente.trim().toUpperCase().replace(/\s/g, '')

  // Formato antiguo: 3 letras + 3 números (ej: ABC123)
  const formatoAntiguo = /^[A-Z]{3}[0-9]{3}$/

  // Formato nuevo: 2 letras + 3 números + 2 letras (ej: AB123CD)
  const formatoNuevo = /^[A-Z]{2}[0-9]{3}[A-Z]{2}$/

  if (formatoAntiguo.test(patenteLimpia)) {
    return {
      isValid: true,
      format: 'antiguo',
      message: 'Formato válido (antiguo)',
      patenteFormateada: patenteLimpia
    }
  }

  if (formatoNuevo.test(patenteLimpia)) {
    return {
      isValid: true,
      format: 'nuevo',
      message: 'Formato válido (nuevo)',
      patenteFormateada: patenteLimpia
    }
  }

  return {
    isValid: false,
    format: null,
    message: 'Formato inválido. Use: ABC123 (antiguo) o AB123CD (nuevo)'
  }
}

/**
 * Formatea la patente mientras el usuario escribe
 * @param {string} value - Valor actual del input
 * @returns {string} - Patente formateada
 */
export const formatearPatenteInput = (value) => {
  // Remover todo excepto letras y números
  const limpia = value.replace(/[^A-Za-z0-9]/g, '').toUpperCase()

  // Si tiene 6 caracteres o menos, podría ser formato antiguo
  if (limpia.length <= 6) {
    return limpia
  }

  // Si tiene más de 6, podría ser formato nuevo
  // Formato: AB123CD (sin espacios) o AB 123 CD (con espacios)
  if (limpia.length <= 7) {
    return limpia
  }

  return limpia.substring(0, 7)
}

