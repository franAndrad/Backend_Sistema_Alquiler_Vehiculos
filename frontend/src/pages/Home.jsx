import { Link } from 'react-router-dom'
import './Home.css'

function Home() {
  return (
    <div className="home">
      <div className="home-hero">
        <h2>Bienvenido al Sistema de Alquiler de Vehículos</h2>
        <p>Gestión integral de vehículos, clientes, alquileres y más</p>
      </div>

      <div className="home-grid">
        <Link to="/clientes" className="home-card">
          <h3>👥 Clientes</h3>
          <p>Gestionar clientes del sistema</p>
        </Link>

        <Link to="/vehiculos" className="home-card">
          <h3>🚗 Vehículos</h3>
          <p>Administrar flota de vehículos</p>
        </Link>

        <Link to="/alquileres" className="home-card">
          <h3>📋 Alquileres</h3>
          <p>Gestionar alquileres activos</p>
        </Link>

        <Link to="/reservas" className="home-card">
          <h3>📅 Reservas</h3>
          <p>Administrar reservas de vehículos</p>
        </Link>

        <Link to="/empleados" className="home-card">
          <h3>👔 Empleados</h3>
          <p>Gestionar personal</p>
        </Link>

        <Link to="/marcas" className="home-card">
          <h3>🏷️ Marcas</h3>
          <p>Administrar marcas de vehículos</p>
        </Link>

        <Link to="/modelos" className="home-card">
          <h3>🔧 Modelos</h3>
          <p>Gestionar modelos de vehículos</p>
        </Link>

        <Link to="/multas" className="home-card">
          <h3>⚠️ Multas</h3>
          <p>Administrar multas de alquileres</p>
        </Link>
      </div>
    </div>
  )
}

export default Home

