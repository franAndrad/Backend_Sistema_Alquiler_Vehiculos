# Sistema de Gestión de Alquileres

Backend desarrollado en **Flask**, **MySQL**, **SQLAlchemy**, **JWT** y un ecosistema de patrones orientados a objetos. El proyecto implementa una arquitectura modular, escalable y mantenible, ideal para entornos productivos y académicos.

---

# 🧩 Arquitectura General

El proyecto está organizado en capas:

* **Controllers**: manejo de endpoints HTTP.
* **Services**: lógica de negocio.
* **Repository**: acceso a datos (SQLAlchemy ORM).
* **Models**: entidades y enums.
* **Utils**: validaciones, autenticación y mappers.
* **Patterns**: uso de **Singleton**, **State** y **Observer**.

---

# 🧠 Patrones de Diseño Implementados

## 🟦 Singleton — Inicialización de la Base de Datos

Asegura que:

* La base se inicialice **una sola vez**.
* Se eviten condiciones de carrera.
* Exista una única instancia consistente para todo el sistema.

Ideal para entornos Docker donde los contenedores pueden iniciar en paralelo.

---

## 🟩 State — Gestión de Estados del Dominio

Implementado en:

* **Vehículos**
* **Reservas**
* **Alquileres**

### Beneficios

* Cada estado define su propio comportamiento.
* Evita condicionales complejos.
* No permite transiciones inválidas.

### Ejemplos

* Un vehículo `ALQUILADO` **no puede volver** a `RESERVADO`.
* Una reserva `EXPIRADA` **no puede cancelarse**.
* Un alquiler `FINALIZADO` **no puede modificarse**.

---

## 🟧 Observer — Sistema Global de Notificaciones

Se implementó un **notificador global** basado en el patrón Observer.

### ¿Qué hace?

Cada vez que se crea:

* una **Reserva**, o
* un **Alquiler**,

se dispara un evento que ejecuta automáticamente todos los observers registrados.

### Observers actuales

* **EmailClienteObserver**: envía correo al cliente.
* **SMSObserver**: envía SMS (simulado por consola).
* *Se pueden agregar más observers fácilmente*: EmailEmpleadosObserver, WhatsAppObserver, LoggerObserver, etc.

### Flujo del Observer

1. Se crea una Reserva o un Alquiler.
2. El service ejecuta `notificador_movimientos.notificar(entidad)`.
3. El notificador global (Singleton) llama a cada observer.
4. Cada observer realiza su trabajo sin modificar los services.

### Ventajas

* Notificaciones centralizadas.
* No se repite lógica.
* Fácil de extender.
* Funciona con **cualquier entidad** que tenga cliente, vehículo, fecha_inicio, fecha_fin.

---

# 🚀 Cómo iniciar el proyecto

## 1) Con Docker (recomendado)

```bash
docker compose build --no-cache
docker compose up
```

### Servicios

| Servicio       | Puerto | Descripción |
| -------------- | ------ | ----------- |
| alquileres_api | 5000   | API Flask   |
| alquileres_db  | 3306   | MySQL 8     |

---

## 2) Ejecutar localmente

### Crear entorno virtual

```bash
python -m venv venv
```

### Activarlo

Linux / macOS:

```bash
source venv/bin/activate
```

Windows (PowerShell):

```bash
.\venv\Scripts\Activate.ps1
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Archivo `.env` requerido

```env
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=tp

JWT_SECRET_KEY=super_key_123
JWT_EXPIRES_IN=900

# Opcional: Email via Mailtrap
MAIL_SERVER=smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=xxxxxx
MAIL_PASSWORD=yyyyyy
MAIL_DEFAULT_SENDER=noreply@alquileres.com
```

Ejecutar:

```bash
python app.py
```

La API estará disponible en:
**[http://localhost:5000](http://localhost:5000)**

---

# 🔐 Autenticación

### POST `/auth/login`

Genera un token JWT.

### GET `/auth/me`

Devuelve la información del usuario autenticado.

---

# 📡 Endpoints disponibles

A continuación se detalla el listado completo de endpoints por recurso y rol permitido.

## 🧑 Empleados (`/empleados`)

| Método | Endpoint                 | Acción           | Roles |
| ------ | ------------------------ | ---------------- | ----- |
| GET    | /empleados               | Listar           | ADMIN |
| GET    | /empleados/rol/{rol}     | Listar por rol   | ADMIN |
| GET    | /empleados/{id}          | Obtener          | ADMIN |
| GET    | /empleados/dni/{dni}     | Buscar por DNI   | ADMIN |
| GET    | /empleados/email/{email} | Buscar por email | ADMIN |
| POST   | /empleados               | Crear            | ADMIN |
| PUT    | /empleados/{id}          | Actualizar       | ADMIN |
| DELETE | /empleados/{id}          | Eliminar         | ADMIN |

---

## 👤 Clientes (`/clientes`)

| Método | Endpoint                | Acción           | Roles            |
| ------ | ----------------------- | ---------------- | ---------------- |
| GET    | /clientes               | Listar           | ADMIN            |
| GET    | /clientes/{id}          | Obtener          | ADMIN / ATENCION |
| POST   | /clientes               | Crear            | ADMIN / ATENCION |
| PUT    | /clientes/{id}          | Actualizar       | ADMIN / ATENCION |
| DELETE | /clientes/{id}          | Eliminar         | ADMIN            |
| GET    | /clientes/dni/{dni}     | Buscar por DNI   | ADMIN / ATENCION |
| GET    | /clientes/email/{email} | Buscar por email | ADMIN / ATENCION |

---

## 🚗 Vehículos (`/vehiculos`)

| Método | Endpoint                    | Acción            | Roles            |
| ------ | --------------------------- | ----------------- | ---------------- |
| GET    | /vehiculos                  | Listar            | ADMIN / ATENCION |
| GET    | /vehiculos/{id}             | Obtener           | ADMIN / ATENCION |
| GET    | /vehiculos/estado/{estados} | Buscar por estado | ADMIN / ATENCION |
| POST   | /vehiculos                  | Crear             | ADMIN            |
| PUT    | /vehiculos/{id}             | Actualizar        | ADMIN            |
| DELETE | /vehiculos/{id}             | Eliminar          | ADMIN            |

---

## 📅 Reservas (`/reservas`)

| Método | Endpoint                       | Acción            | Roles            |
| ------ | ------------------------------ | ----------------- | ---------------- |
| GET    | /reservas                      | Listar            | ADMIN / ATENCION |
| GET    | /reservas/{id}                 | Obtener           | ADMIN / ATENCION |
| GET    | /reservas/estado/{estados}     | Buscar por estado | ADMIN / ATENCION |
| GET    | /reservas/cliente/{cliente_id} | Por cliente       | ADMIN / ATENCION |
| POST   | /reservas                      | Crear             | ADMIN / ATENCION |
| PUT    | /reservas/{id}                 | Actualizar        | ADMIN / ATENCION |
| PATCH  | /reservas/{id}/cancelar        | Cancelar          | ADMIN / ATENCION |

---

## 🚨 Multas (`/multas`)

| Método | Endpoint     | Acción     | Roles            |
| ------ | ------------ | ---------- | ---------------- |
| GET    | /multas      | Listar     | ADMIN / ATENCION |
| GET    | /multas/{id} | Obtener    | ADMIN / ATENCION |
| POST   | /multas      | Crear      | ADMIN / ATENCION |
| PUT    | /multas/{id} | Actualizar | ADMIN / ATENCION |
| DELETE | /multas/{id} | Eliminar   | ADMIN            |

---

## 🏭 Modelos (`/modelos`)

| Método | Endpoint      | Acción     | Roles |
| ------ | ------------- | ---------- | ----- |
| GET    | /modelos      | Listar     | ADMIN |
| GET    | /modelos/{id} | Obtener    | ADMIN |
| POST   | /modelos      | Crear      | ADMIN |
| PUT    | /modelos/{id} | Actualizar | ADMIN |
| DELETE | /modelos/{id} | Eliminar   | ADMIN |

---

## 🏷️ Marcas (`/marcas`)

| Método | Endpoint                | Acción            | Roles |
| ------ | ----------------------- | ----------------- | ----- |
| GET    | /marcas                 | Listar            | ADMIN |
| GET    | /marcas/{id}            | Obtener           | ADMIN |
| GET    | /marcas/nombre/{nombre} | Buscar por nombre | ADMIN |
| POST   | /marcas                 | Crear             | ADMIN |
| PUT    | /marcas/{id}            | Actual            |       |
