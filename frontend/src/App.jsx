import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Clientes from './pages/Clientes'
import Vehiculos from './pages/Vehiculos'
import Alquileres from './pages/Alquileres'
import Reservas from './pages/Reservas'
import Empleados from './pages/Empleados'
import Marcas from './pages/Marcas'
import Modelos from './pages/Modelos'
import Multas from './pages/Multas'
import './App.css'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/clientes" element={<Clientes />} />
          <Route path="/vehiculos" element={<Vehiculos />} />
          <Route path="/alquileres" element={<Alquileres />} />
          <Route path="/reservas" element={<Reservas />} />
          <Route path="/empleados" element={<Empleados />} />
          <Route path="/marcas" element={<Marcas />} />
          <Route path="/modelos" element={<Modelos />} />
          <Route path="/multas" element={<Multas />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App

