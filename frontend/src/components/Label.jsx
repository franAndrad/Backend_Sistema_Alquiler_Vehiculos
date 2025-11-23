/**
 * Componente de label con soporte para asterisco rojo en campos obligatorios
 */
function Label({ children, required = false, htmlFor }) {
  return (
    <label htmlFor={htmlFor}>
      {children}
      {required && <span className="required-asterisk"> *</span>}
    </label>
  )
}

export default Label

