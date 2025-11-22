# Sistema de Gestión de Alquileres

Backend desarrollado en **Flask**, **MySQL** y **JWT**, con estructura modular basada en:
- **Controllers**: manejo de endpoints HTTP.
- **Services**: reglas de negocio.
- **Repository**: acceso a datos.
- **Models**: entidades y enums.
- **Utils**: validaciones, autenticación y mappers.
- **Patterns**: uso de **Singleton** y **State** para mejorar la mantenibilidad.

---

# 🧩 Patrones utilizados

## 🟦 Patrón Singleton — Inicialización de la Base de Datos

La clase encargada de inicializar la base de datos implementa un **Singleton**, garantizando que:
- La inicialización solo ocurra una vez.
- Se eviten condiciones de carrera.
- Todas las capas del sistema utilicen la misma instancia.

Esto asegura consistencia durante el arranque del sistema, especialmente dentro de Docker.

---

## 🟩 Patrón State — Gestión de Estados del Dominio

Se aplica en:
- Vehículos  
- Reservas  
- Alquileres  

Cada estado define su propio comportamiento y restricciones, evitando el uso de condicionales extensos.

Ejemplos:
- Un vehículo `ALQUILADO` no puede volver a `RESERVADO`.
- Una reserva `EXPIRADA` no puede ser cancelada.
- Un alquiler `FINALIZADO` ya no puede modificarse.

Esto permite reglas claras, extensibles y encapsuladas.

---

## 🚀 Cómo iniciar el proyecto

### 1) Con Docker (recomendado)

```bash
docker compose build --no-cache
docker compose up
```

Servicios:

| Servicio         | Puerto | Descripción |
|-----------------|--------|-------------|
| alquileres_api  | 5000   | API Flask   |
| alquileres_db   | 3306   | MySQL 8     |

---

### 2) Ejecutar localmente

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.app
```

---

# 🔐 Autenticación

### POST `/auth/login`
Devuelve: **JWT**.

### GET `/auth/me`
Requiere autenticación. Devuelve datos del usuario autenticado.

---

# 📡 Endpoints y Permisos por Rol

A continuación se listan **todos los endpoints reales presentes en tu código**, incluyendo los nuevos:

---

# 🧑 Empleados (`/empleados`)

| Método | Endpoint | Acción | Roles |
|--------|----------|--------|--------|
| GET | /empleados | Listar empleados | ADMIN |
| GET | /empleados/rol/{rol} | Listar por rol | ADMIN |
| GET | /empleados/{id} | Obtener empleado | ADMIN |
| GET | /empleados/dni/{dni} | Obtener por DNI | ADMIN |
| GET | /empleados/email/{email} | Obtener por email | ADMIN |
| POST | /empleados | Crear | ADMIN |
| PUT | /empleados/{id} | Actualizar | ADMIN |
| DELETE | /empleados/{id} | Eliminar | ADMIN |

---

# 👤 Clientes (`/clientes`)

| Método | Endpoint | Acción | Roles |
|--------|-----------|--------|--------|
| GET | /clientes | Listar clientes | ADMIN |
| GET | /clientes/{id} | Obtener cliente | ADMIN / ATENCION |
| POST | /clientes | Crear cliente | ADMIN / ATENCION |
| PUT | /clientes/{id} | Actualizar | ADMIN / ATENCION |
| DELETE | /clientes/{id} | Eliminar | ADMIN |
| GET | /clientes/dni/{dni} | Buscar por DNI | ADMIN / ATENCION |
| GET | /clientes/email/{email} | Buscar por email | ADMIN / ATENCION |

---

# 🚗 Vehículos (`/vehiculos`)

**Actualizado según tu código 👇**

| Método | Endpoint | Acción | Roles |
|--------|-----------|--------|--------|
| GET | /vehiculos | Listar | ADMIN / ATENCION |
| GET | /vehiculos/{id} | Obtener | ADMIN / ATENCION |
| GET | /vehiculos/estado/{estados} | Buscar por estado (lista separada por comas) | ADMIN / ATENCION |
| POST | /vehiculos | Crear | ADMIN |
| PUT | /vehiculos/{id} | Actualizar | ADMIN |
| DELETE | /vehiculos/{id} | Eliminar | ADMIN |

---

# 📅 Reservas (`/reservas`)

**Actualizado también según tu código 👇**

| Método | Endpoint | Acción | Roles |
|--------|-----------|--------|--------|
| GET | /reservas | Listar reservas | ADMIN / ATENCION |
| GET | /reservas/{id} | Obtener reserva | ADMIN / ATENCION |
| GET | /reservas/estado/{estados} | Obtener por estado | ADMIN / ATENCION |
| GET | /reservas/cliente/{cliente_id} | Reservas de un cliente | ADMIN / ATENCION |
| POST | /reservas | Crear | ADMIN / ATENCION |
| PUT | /reservas/{id} | Actualizar | ADMIN / ATENCION |
| PATCH | /reservas/{id}/cancelar | Cancelar | ADMIN / ATENCION |

---

# 🚨 Multas (`/multas`)

**Actualizado 👇**

| Método | Endpoint | Acción | Roles |
|--------|-----------|--------|--------|
| GET | /multas | Listar | ADMIN / ATENCION |
| GET | /multas/{id} | Obtener multa | ADMIN / ATENCION |
| POST | /multas | Crear | ADMIN / ATENCION |
| PUT | /multas/{id} | Actualizar | ADMIN / ATENCION |
| DELETE | /multas/{id} | Eliminar | ADMIN |

---

# 🏭 Modelos (`/modelos`)

| Método | Endpoint | Acción | Roles |
|--------|-----------|--------|--------|
| GET | /modelos | Listar | ADMIN |
| GET | /modelos/{id} | Obtener | ADMIN |
| POST | /modelos | Crear | ADMIN |
| PUT | /modelos/{id} | Actualizar | ADMIN |
| DELETE | /modelos/{id} | Eliminar | ADMIN |

---

# 🏷️ Marcas (`/marcas`)

| Método | Endpoint | Acción | Roles |
|--------|-----------|--------|--------|
| GET | /marcas | Listar | ADMIN |
| GET | /marcas/{id} | Obtener | ADMIN |
| GET | /marcas/nombre/{nombre} | Buscar por nombre | ADMIN |
| POST | /marcas | Crear | ADMIN |
| PUT | /marcas/{id} | Actualizar | ADMIN |
| DELETE | /marcas/{id} | Eliminar | ADMIN |

---

# 📏 Reglas de negocio (resumen)

## Empleados
- DNI y email únicos.
- Password en hash.
- Solo ADMIN gestiona empleados.

## Clientes
- Validación estricta de DNI, email, licencia vigente.

## Vehículos
- Estados: `DISPONIBLE`, `RESERVADO`, `ALQUILADO`.
- No se puede crear reserva ni alquiler si el vehículo no está disponible.
- Búsqueda por múltiples estados: `/vehiculos/estado/DISPONIBLE,RESERVADO`

## Reservas
- Expiran si no se confirman.
- Cancelación por PATCH.
- Reservas por estado y cliente.

## Multas
- Asociadas a un alquiler.
- Eliminación SOLO por ADMIN.

---

# ✔️ Validaciones faltantes recomendadas

- Complejidad mínima de contraseña.
- Evitar eliminar empleados con alquileres asociados.
- Evitar quedar sin un ADMIN en el sistema.
- Validación más estricta de teléfono y longitudes de campos.

---
