import { Link, useLocation } from 'react-router-dom'
import './Layout.css'

function Layout({ children }) {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Inicio' },
    { path: '/clientes', label: 'Clientes' },
    { path: '/vehiculos', label: 'Vehículos' },
    { path: '/alquileres', label: 'Alquileres' },
    { path: '/reservas', label: 'Reservas' },
    { path: '/empleados', label: 'Empleados' },
    { path: '/marcas', label: 'Marcas' },
    { path: '/modelos', label: 'Modelos' },
    { path: '/multas', label: 'Multas' },
  ]

  return (
    <div className="layout">
      <header className="header">
        <h1>🚗 Sistema de Alquiler de Vehículos</h1>
        <nav className="nav">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={location.pathname === item.path ? 'active' : ''}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </header>
      <main className="main-content">
        {children}
      </main>
    </div>
  )
}

export default Layout

