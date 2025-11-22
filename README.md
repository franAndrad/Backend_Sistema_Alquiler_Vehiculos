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

# 📡 Endpoints y Roles

...

(El resto del contenido va igual al del mensaje anterior)

