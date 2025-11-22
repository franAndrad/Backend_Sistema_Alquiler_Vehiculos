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
Se utiliza para garantizar:
- Que la inicialización ocurra **una sola vez**.
- Evitar condiciones de carrera.
- Mantener una única instancia consistente en todo el sistema.

Ideal para entornos Docker donde los servicios pueden intentar iniciar simultáneamente.

---

## 🟩 Patrón State — Gestión de Estados del Dominio
Implementado en:
- Vehículos  
- Reservas  
- Alquileres  

Ventajas:
- Evita condicionales complejos.
- Cada estado define su comportamiento.
- No se permiten transiciones inválidas (ej. finalizar un alquiler ya finalizado).

Ejemplos:
- Vehículo `ALQUILADO` no puede volver a `RESERVADO`.
- Reserva `EXPIRADA` no puede cancelarse.
- Alquiler `FINALIZADO` no puede modificarse.

---

# 🚀 Cómo iniciar el proyecto

## 1) Con Docker (recomendado)
```bash
docker compose build --no-cache
docker compose up
```

| Servicio         | Puerto | Descripción |
|-----------------|--------|-------------|
| alquileres_api  | 5000   | API Flask   |
| alquileres_db   | 3306   | MySQL 8     |

---

## 2) Ejecutar localmente
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.app
```

---

# 🔐 Autenticación

### POST `/auth/login`
Devuelve un token **JWT**.

### GET `/auth/me`
Requiere token. Devuelve info del usuario autenticado.

---

# 📡 Endpoints y Permisos por Rol
Listado completo basado en tu código real.

---

# 🧑 Empleados (`/empleados`)

| Método | Endpoint | Acción | Roles |
|--------|----------|--------|--------|
| GET | /empleados | Listar | ADMIN |
| GET | /empleados/rol/{rol} | Listar por rol | ADMIN |
| GET | /empleados/{id} | Obtener | ADMIN |
| GET | /empleados/dni/{dni} | Buscar por DNI | ADMIN |
| GET | /empleados/email/{email} | Buscar por email | ADMIN |
| POST | /empleados | Crear | ADMIN |
| PUT | /empleados/{id} | Actualizar | ADMIN |
| DELETE | /empleados/{id} | Eliminar | ADMIN |

---

# 👤 Clientes (`/clientes`)

| Método | Endpoint | Acción | Roles |
|--------|-----------|--------|--------|
| GET | /clientes | Listar | ADMIN |
| GET | /clientes/{id} | Obtener | ADMIN / ATENCION |
| POST | /clientes | Crear | ADMIN / ATENCION |
| PUT | /clientes/{id} | Actualizar | ADMIN / ATENCION |
| DELETE | /clientes/{id} | Eliminar | ADMIN |
| GET | /clientes/dni/{dni} | Buscar por DNI | ADMIN / ATENCION |
| GET | /clientes/email/{email} | Buscar por email | ADMIN / ATENCION |

---

# 🚗 Vehículos (`/vehiculos`)

| Método | Endpoint | Acción | Roles |
|--------|-----------|--------|--------|
| GET | /vehiculos | Listar | ADMIN / ATENCION |
| GET | /vehiculos/{id} | Obtener | ADMIN / ATENCION |
| GET | /vehiculos/estado/{estados} | Buscar por estado | ADMIN / ATENCION |
| POST | /vehiculos | Crear | ADMIN |
| PUT | /vehiculos/{id} | Actualizar | ADMIN |
| DELETE | /vehiculos/{id} | Eliminar | ADMIN |

---

# 📅 Reservas (`/reservas`)

| Método | Endpoint | Acción | Roles |
|--------|-----------|--------|--------|
| GET | /reservas | Listar | ADMIN / ATENCION |
| GET | /reservas/{id} | Obtener | ADMIN / ATENCION |
| GET | /reservas/estado/{estados} | Buscar por estado | ADMIN / ATENCION |
| GET | /reservas/cliente/{cliente_id} | Por cliente | ADMIN / ATENCION |
| POST | /reservas | Crear | ADMIN / ATENCION |
| PUT | /reservas/{id} | Actualizar | ADMIN / ATENCION |
| PATCH | /reservas/{id}/cancelar | Cancelar | ADMIN / ATENCION |

---

# 🚨 Multas (`/multas`)

| Método | Endpoint | Acción | Roles |
|--------|-----------|--------|--------|
| GET | /multas | Listar | ADMIN / ATENCION |
| GET | /multas/{id} | Obtener | ADMIN / ATENCION |
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

# 🚚 Alquileres (`/alquileres`)

| Método | Endpoint | Acción | Roles |
|--------|-----------|--------|--------|
| GET | /alquileres | Listar | ADMIN / ATENCION |
| GET | /alquileres/{id} | Obtener | ADMIN / ATENCION |
| GET | /alquileres/cliente/{cliente_id} | Por cliente | ADMIN / ATENCION |
| GET | /alquileres/vehiculo/{vehiculo_id} | Por vehículo | ADMIN / ATENCION |
| GET | /alquileres/estado/{estados} | Por estado | ADMIN / ATENCION |
| GET | /alquileres/periodo?desde=X&hasta=Y | Por período | ADMIN / ATENCION |
| GET | /alquileres/vehiculos-mas-alquilados | Ranking | ADMIN / ATENCION |
| POST | /alquileres | Crear | ADMIN / ATENCION |
| PUT | /alquileres/{id} | Actualizar | ADMIN / ATENCION |
| PATCH | /alquileres/{id}/finalizar | Finalizar | ADMIN / ATENCION |

---

# 📏 Reglas de negocio

## Empleados
- DNI + email únicos.
- Contraseña hasheada.
- Solo ADMIN gestiona empleados.

## Clientes
- Validación estricta de DNI, email y licencia.

## Vehículos
- Estados manejados con **State**.
- Disponibilidad controlada.
- No se alquila ni reserva si no está DISPONIBLE.

## Reservas
- Expiran automáticamente.
- Cancelación con PATCH.
- Filtrado por cliente y estado.

## Alquileres
- Solo se finalizan si están activos.
- Finalización calcula monto.
- Estadísticas por período y por vehículo.
- Relación entre Reserva y Alquiler:

    - Si existe una reserva para un vehículo en un período determinado, solo puede generarse un alquiler dentro de ese mismo período.

    - Si el cliente intenta alquilar ANTES del inicio del período reservado, se permite el alquiler pero la reserva se ignora, ya que el cliente está alquilando anticipadamente.

    - Si el cliente intenta alquilar DESPUÉS del período reservado, la reserva expira automáticamente (su estado pasa a EXPIRADA) y no se utiliza para el alquiler.

    - Garantiza que un vehículo reservado queda bloqueado para ese período, pero no impide alquilarlo antes si el cliente lo solicita.
    
    - La reserva solo sirve como “bloqueo” del período reservado; fuera del período, se toma la decisión correcta según el caso:

        - Antes → se ignora
        - Después → expira

## Multas
- Asociadas a alquiler.
- Solo ADMIN puede eliminar.

---

# ✔ Validaciones faltantes recomendadas
- Políticas de contraseñas más seguras.
- Evitar eliminar empleados referenciados.
- Evitar quedarse sin un usuario ADMIN.
- Validaciones extra para teléfonos y longitudes.

---

