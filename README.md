# 🚗 Sistema de Alquiler de Vehículos - Grupo 33

Este proyecto es el trabajo práctico integrador para la materia "Desarrollo de Aplicaciones con Objetos". El objetivo es construir una aplicación web de gestión integral para una empresa de alquiler de vehículos.

## 🎯 Objetivos del Sistema

### Objetivo General
[cite_start]Desarrollar una aplicación de gestión integral que permita administrar la flota, los clientes y el proceso de alquiler de forma eficiente[cite: 7].

### Objetivos Específicos
* [cite_start]Implementar las operaciones **CRUD** (Altas, Bajas, Modificaciones y Consultas) para Vehículos, Clientes y Empleados[cite: 9].
* [cite_start]Gestionar la transacción principal de **"Alquiler"**, validando la disponibilidad de los vehículos[cite: 10, 21].
* [cite_start]Proveer **reportes** y estadísticas sobre la operación (ej. vehículos más alquilados, facturación)[cite: 11].

---

## 🛠️ Stack Tecnológico y Requerimientos

Este proyecto utiliza un stack simple pero potente para aplicar los conceptos de POO y desarrollo web:

* **Python:** Como lenguaje principal de programación.
* **Flask:** Un "micro-framework" web. Lo usamos para construir nuestros **Controladores** (recibir peticiones HTTP de las URLs) y renderizar las **Vistas** (plantillas HTML).
* **SQLite:** Un motor de base de datos relacional ligero basado en archivos. Lo usamos como nuestro **Modelo** para persistir los datos de la aplicación (vehículos, clientes, etc.).

### Archivo de Requerimientos
Para instalar las dependencias, asegúrate de que tu archivo `requirements.txt` contenga:

```txt
Flask
```

---

## 🚀 Cómo Empezar

Sigue estos pasos para levantar el entorno de desarrollo local:

1.  **Crear un Entorno Virtual** (Recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

2.  **Instalar Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Inicializar la Base de Datos**:
    (Solo necesitas hacerlo la primera vez, o si borras `alquileres.db`)
    ```bash
    python init_database.py
    ```

4.  **Ejecutar el Servidor**:
    ```bash
    python run.py
    ```

5.  **Abrir la Aplicación**:
    Visita `http://127.0.0.1:5000/` en tu navegador.

---

## 📁 Estructura del Proyecto

El proyecto está organizado siguiendo el patrón arquitectónico **MVC (Modelo-Vista-Controlador)** y utiliza un patrón **Application Factory** para inicializar Flask.

```
## 📁 Estructura del Proyecto


/tpDAOSistemaDelquilerDeVehiculo/
|
|-- /sistema/                <-- Paquete principal de la aplicación Flask
|   |-- __init__.py          # Define la "Application Factory" (create_app)
|   |                        # e inicializa el objeto 'db' de SQLAlchemy.
|   |
|   |-- /controllers/        <-- (C) CONTROLADORES (Lógica de Rutas)
|   |   |-- __init__.py      # (Vacío)
|   |   |-- main_controller.py   # Blueprint para rutas principales (/, /index)
|   |
|   |-- /models/             <-- (M) MODELOS (Lógica de Negocio y Datos)
|   |   |-- __init__.py      # (Vacío)
|   |   |-- marca.py         # Clase Marca
|   |   |-- modelo.py        # Clase Modelo
|   |   |-- vehiculo.py      # Clase Vehiculo (aquí irá el Patrón State)
|   |   |-- cliente.py       # Clase Cliente
|   |   |-- empleado.py      # Clase Empleado
|   |   |-- alquiler.py      # Clase Alquiler (Transacción principal)
|   |
|   |-- /templates/          <-- (V) VISTAS (Plantillas HTML)
|   |   |-- index.html
|   |
|   |-- /static/             <-- Archivos estáticos (CSS, JS, imágenes)
|
|-- run.py                   # Script de arranque (Llama a create_app() e inicia el servidor)
|-- init_database.py         # Script para crear y poblar la BD usando SQLAlchemy (db.create_all())
|-- alquileres.db            # Archivo de la BD (creado por init_database.py)
|-- requirements.txt         # Lista de dependencias de Python (Flask, Flask-SQLAlchemy)
|-- .gitignore               # Ignora archivos (como venv/, __pycache__/, alquileres.db)
|-- README.md                # Esta documentación
```


---

## 🏛️ Arquitectura y Decisiones de Diseño

Esta sección explica las decisiones de arquitectura de software tomadas para el proyecto, por qué se eligieron y cómo funcionan.

### 1. El Patrón "Application Factory"

En lugar de crear la instancia de la aplicación Flask (`app`) de forma global en `sistema/__init__.py`, usamos una función `create_app()`.

**El Problema que Resuelve: Importaciones Circulares**

En una aplicación Flask, es común tener un "callejón sin salida" (una importación circular):
1.  El archivo `__init__.py` necesita crear `app` y `db` (la base de datos).
2.  Para crear la base de datos, `__init__.py` necesita importar los Modelos (ej. `Vehiculo`, `Cliente`).
3.  Pero los archivos de Modelos (ej. `vehiculo.py`) necesitan importar el objeto `db` desde `__init__.py` para poder heredar de `db.Model`.

Python no puede resolver este círculo (Archivo A importa Archivo B, y Archivo B importa Archivo A).

**La Solución (La Fábrica):**
1.  **`sistema/__init__.py`** solo crea un objeto `db = SQLAlchemy()` **vacío y desconectado**.
2.  Los Modelos (`vehiculo.py`, `cliente.py`, etc.) importan este `db` vacío sin problemas.
3.  **`run.py`** (el script de inicio) llama a la función `create_app()`.
4.  **Dentro de `create_app()`**, se crea la `app` y *luego* se conecta al objeto `db` usando `db.init_app(app)`. Finalmente, se registran los controladores (Blueprints).

Esto rompe el ciclo y nos da una forma limpia y robusta de inicializar la aplicación.

### 2. El Rol de los Modelos (Patrón "Active Record")

Como notaste, nuestras clases en `/models/` tienen una doble responsabilidad. Este enfoque se conoce como el patrón **Active Record**.

* **1. Rol de Mapeo (Similar a un Repositorio):** Heredan de `db.Model`, lo que le da a SQLAlchemy la información para "mapear" la clase a una tabla de la base de datos.
* **2. Rol de Objeto de Negocio:** También contienen la lógica de negocio (métodos). Aquí es donde implementaremos el **Patrón State** (`alquilar()`, `devolver()`), el **Patrón Strategy** (para calcular costos), etc.

**¿Por qué este enfoque?**
Para este proyecto, mantiene la lógica de negocio y la persistencia de datos juntas, haciendo el código más simple y directo, lo cual es ideal para enfocarnos en los patrones de POO.

**Escalabilidad a Futuro:**
Tienes razón, en sistemas más grandes, estas responsabilidades se suelen separar usando el **"Patrón Repository"**. En ese diseño, tendríamos una clase `Vehiculo` (POO pura, sin `db.Model`) y una clase `VehiculoRepository` separada, cuyo único trabajo sería guardar y leer objetos `Vehiculo` de la base de datos.

### 3. SQLAlchemy: El "Antes y Después" del ORM

El cambio a SQLAlchemy (un Mapeador Objeto-Relacional u ORM) nos libera de escribir SQL a mano y nos permite pensar solo en objetos.

#### Antes: CRUD Manual (sin ORM)

Antes del refactor, teníamos que manejar la conexión y escribir SQL manualmente en cada modelo.

```python
# --- ANTES ---
from sistema.database import get_db_connection

class Vehiculo:
    def __init__(self, patente, ...):
        # ...
    
    def _crear(self):
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO vehiculos (patente, ...) VALUES (?, ...)",
                (self.patente, ...)
            )
            conn.commit()

    @staticmethod
    def obtener_por_id(id):
        with get_db_connection() as conn:
            fila = conn.execute("SELECT * FROM vehiculos WHERE id = ?", (id,)).fetchone()
            if fila:
                return Vehiculo(fila['patente'], ...)
# --- DESPUÉS ---
from sistema import db # Importamos el objeto ORM

class Vehiculo(db.Model):
    # El ORM sabe que esto es una tabla
    __tablename__ = 'vehiculos'
    
    # El ORM sabe que esto es una columna
    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(10), unique=True)
    
    # Aquí irá la lógica (Patrón State)
    def alquilar(self):
        # ...
    
# --- Cómo usamos el CRUD ahora (en los controladores) ---

# Crear:
auto_nuevo = Vehiculo(patente='AA123BB', ...)
db.session.add(auto_nuevo)
db.session.commit()

# Leer:
auto = Vehiculo.query.get(1)
todos_los_autos = Vehiculo.query.all()

# Actualizar:
auto = Vehiculo.query.get(1)
auto.estado = 'Alquilado'
db.session.commit()
```


---

## 🎨 Patrones de Diseño Aplicados (ESTO TODAVIA REVISAR)

[cite_start]Además de MVC, el proyecto busca implementar patrones de diseño de POO para resolver problemas comunes[cite: 13]:

1.  **Patrón State (Estado)**:
    * [cite_start]**Problema:** Un `Vehiculo` tiene estados que cambian su comportamiento (ej. "Disponible", "Alquilado", "En Mantenimiento")[cite: 21]. No queremos `if/else` gigantes en la clase `Vehiculo`.
    * **Solución:** Crearemos una interfaz `EstadoVehiculo` y clases concretas (`EstadoDisponible`, `EstadoAlquilado`). La clase `Vehiculo` *delegará* el comportamiento (como `alquilar()` o `devolver()`) a su objeto de estado actual.

2.  **Patrón Factory (Fábrica)**:
    * [cite_start]**Problema:** El sistema necesita generar diferentes tipos de reportes (ej. "Alquileres por Cliente", "Vehículos Más Alquilados")[cite: 11, 26, 28].
    * **Solución:** Crearemos una `ReportFactory` que reciba un tipo de reporte y devuelva el objeto de reporte correcto, listo para ser procesado.

3.  **Patrón Strategy (Estrategia)**:
    * [cite_start]**Problema:** El cálculo del costo de un alquiler puede cambiar[cite: 23]. Podríamos tener una tarifa diaria simple, una tarifa con descuento por semana, o una tarifa especial de fin de semana.
    * **Solución:** Crearemos una interfaz `EstrategiaDeCalculo` y clases concretas (`CalculoTarifaDiaria`, `CalculoTarifaSemanal`). La clase `Alquiler` usará una de estas estrategias para determinar el `costo_total` sin que la clase `Alquiler` sepa los detalles del cálculo.