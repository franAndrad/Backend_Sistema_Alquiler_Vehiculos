# Frontend - Sistema de Alquiler de Vehículos

Frontend desarrollado en React para el Sistema de Alquiler de Vehículos.

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Node.js (versión 16 o superior)
- npm o yarn

### Pasos para ejecutar

1. **Instalar dependencias:**
   ```bash
   cd frontend
   npm install
   ```

2. **Ejecutar en modo desarrollo:**
   ```bash
   npm run dev
   ```

3. **Abrir en el navegador:**
   La aplicación estará disponible en `http://localhost:3000`

### Asegúrate de que el backend esté corriendo

El frontend se conecta al backend en `http://localhost:5000`. Asegúrate de que el servidor Flask esté ejecutándose antes de usar la aplicación.

## 📁 Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/      # Componentes reutilizables (Layout, estilos)
│   ├── pages/          # Páginas principales de la aplicación
│   ├── services/       # Servicios API para comunicación con backend
│   ├── App.jsx         # Componente principal con rutas
│   ├── main.jsx        # Punto de entrada
│   └── index.css       # Estilos globales
├── index.html
├── package.json
└── vite.config.js
```

## 🎨 Características

- **CRUD completo** para todas las entidades:
  - Clientes
  - Vehículos
  - Alquileres
  - Reservas
  - Empleados
  - Marcas
  - Modelos
  - Multas

- **Interfaz moderna y responsiva** con diseño limpio
- **Navegación intuitiva** entre secciones
- **Formularios validados** para crear y editar registros
- **Manejo de errores** y estados de carga
- **Filtros** para vehículos por estado

## 🔧 Tecnologías Utilizadas

- **React 18** - Biblioteca de JavaScript para interfaces de usuario
- **React Router** - Enrutamiento para aplicaciones React
- **Vite** - Herramienta de construcción rápida
- **CSS3** - Estilos modernos y responsivos

## 📝 Notas

- El frontend está configurado para conectarse al backend en `http://localhost:5000`
- Si el backend está en otro puerto, modifica `API_BASE_URL` en `src/services/api.js`
- Los estilos están organizados en archivos CSS separados para mejor mantenibilidad

