# MiniLog v4.1

MiniLog es un log de radioaficionado web, liviano y multiusuario, pensado para correr en un VPS o servidor propio dentro de Docker. Permite registrar contactos (QSOs), exportarlos en formato ADIF, y recibir QSOs desde software externo via API REST.

Desarrollado por LU2FTI — [QRZ](https://www.qrz.com/db/LU2FTI)

---

<img width="934" height="515" alt="image" src="https://github.com/user-attachments/assets/cfc6c675-3582-4ad3-9781-ed4c1004d82a" />

---

<img width="1912" height="682" alt="image" src="https://github.com/user-attachments/assets/62585830-fa1f-40fe-b559-6402a01fdfcd" />

---

<img width="1894" height="876" alt="image" src="https://github.com/user-attachments/assets/5005575d-27f2-4587-927e-9b45dbe88b3f" />

---



## Stack

- Python 3.12 + Flask
- Gunicorn como servidor WSGI
- nginx como proxy reverso
- Docker y Docker Compose
- Almacenamiento en CSV por operador (preparado para migrar a SQLite)

---

## Estructura del proyecto

```
minilog/
├── app.py                  # Factory de la aplicación Flask
├── config.py               # Constantes y variables de entorno
├── gunicorn.conf.py        # Configuración de Gunicorn
├── Dockerfile
├── docker-compose.yml
├── cty.dat                 # Base de datos de prefijos DXCC
├── requirements.txt
├── .env.example
├── data/
│   ├── users.json          # Usuarios registrados (callsign + hash de contraseña)
│   ├── reset_tokens.json   # Tokens de reset temporales
│   └── users/
│       └── LU2FTI/
│           └── contacts.csv
├── models/
│   ├── contacts.py
│   └── users.py
├── routes/
│   ├── main.py             # Index, editar, eliminar contactos
│   ├── auth.py             # Login, registro, logout
│   ├── export.py           # Exportacion ADIF
│   ├── lookup.py           # Busqueda DXCC por prefijo
│   ├── api.py              # API REST
│   ├── admin.py            # Panel de administracion
│   ├── profile.py          # Cambio de contraseña
│   └── reset.py            # Reset de contraseña por token
├── storage/
│   ├── base.py             # Interfaz abstracta de storage
│   ├── csv_backend.py      # Implementacion CSV
│   └── __init__.py         # Factory de backend
├── utils/
│   ├── band.py             # Conversion frecuencia a banda
│   └── dxcc.py             # Lookup de pais por prefijo
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── edit.html
│   ├── change_password.html
│   ├── reset_form.html
│   ├── reset_invalid.html
│   └── admin/
│       ├── login.html
│       ├── dashboard.html
│       ├── create_user.html
│       └── reset_link.html
└── nginx/
    └── default.conf
```

---

## Instalacion y deploy

### Requisitos

- Docker
- Docker Compose

### Pasos

1. Clonar o descomprimir el proyecto.

2. Copiar el archivo de variables de entorno y editarlo:

```bash
cp .env.example .env
```

Las variables disponibles son:

```
SECRET_KEY=clave-secreta-larga-y-aleatoria
ADMIN_PASSWORD=contraseña-del-panel-de-admin
STORAGE_BACKEND=csv
```

3. Asegurarse de que `cty.dat` existe en la raiz del proyecto. Este archivo contiene la base de datos de prefijos DXCC y es necesario para la búsqueda de paises.

4. Levantar los contenedores:

```bash
docker compose up -d --build
```

5. La aplicacion queda disponible en `http://tu-servidor:5001`.

---

## Variables de entorno

| Variable         | Descripcion                                      | Default               |
|------------------|--------------------------------------------------|-----------------------|
| SECRET_KEY       | Clave para firmar sesiones Flask                 | changeme-in-production|
| ADMIN_PASSWORD   | Contraseña del panel de administracion           |                       |
| STORAGE_BACKEND  | Backend de almacenamiento: csv (sqlite futuro)   | csv                   |
| BASE_URL         | IP servidor y ip para link de reset password     |                       |

---

## Funcionalidades

### Log de contactos

Desde la pantalla principal se puede registrar un QSO completando callsign, modo, frecuencia y notas opcionales. A medida que se escribe el callsign, el sistema consulta la base de datos DXCC y muestra el pais correspondiente en tiempo real.

Cada contacto queda guardado con fecha y hora UTC automática. La tabla muestra los contactos en orden inverso (el más reciente primero) y permite editar o eliminar cualquier entrada.

El callsign en la tabla es un link directo al perfil del operador en QRZ.com.

### Exportacion ADIF

El boton "Exportar ADIF" genera un archivo `.adi` con todos los contactos del operador autenticado, listo para importar en cualquier software de log compatible con el formato ADIF.

El archivo incluye: callsign propio, callsign del contacto, fecha, hora UTC, banda, frecuencia, modo y notas.

### Multiusuario

Cada operador tiene su propio directorio de datos en `data/users/<CALLSIGN>/contacts.csv`. Los contactos de un operador son completamente independientes de los de otro. Desde la interfaz web cada operador solo ve sus propios QSOs.

### Busqueda DXCC

Al escribir un callsign en el formulario de nuevo contacto, el sistema consulta el archivo `cty.dat` y muestra el pais del operador sin necesidad de hacer submit. La consulta se hace localmente, sin depender de servicios externos.

---

## Auth

### Operadores

El registro es abierto desde `/register`. Cada operador se registra con su callsign y una contraseña. El callsign se almacena en mayúsculas y es el identificador único del operador.

El login esta disponible en `/login`. La sesión se mantiene mediante cookie firmada con `SECRET_KEY`.

### Cambio de contraseña

Un operador autenticado puede cambiar su contraseña desde el botón "Cambiar contraseña" en la pantalla principal, ingresando su contraseña actual y la nueva.

---

## Panel de administración

Accesible en `/admin`. Requiere la contraseña configurada en `ADMIN_PASSWORD`, independiente de las contraseñas de los operadores.

Desde el panel se puede:

- Ver todos los operadores registrados con la cantidad de contactos de cada uno.
- Crear un nuevo operador con callsign y contraseña inicial.
- Eliminar el acceso de un operador (su historial de contactos no se borra).
- Generar un link de reset de contraseña para cualquier operador.

El link de administracion aparece discretamente al pie del formulario de login de operadores.

### Reset de contraseña

El flujo es el siguiente: el administrador genera un link de reset desde el panel para el operador que lo necesita. El link tiene una validez de 30 minutos. El administrador se lo envia al operador por cualquier medio (mensaje, email, radio). El operador abre el link y establece su nueva contraseña sin necesidad de conocer la anterior.

Si el link expiro, muestra una pagina de error indicando que debe solicitar uno nuevo.

---

## API REST

La API permite registrar QSOs desde software externo sin necesidad de iniciar sesion en la interfaz web.

### Autenticacion de la API

Todas las llamadas a la API requieren el siguiente header:

```
Authorization: Bearer HAMRADIOENCASTELLANO
```

Sin este header la API devuelve `401 Unauthorized`.

### Endpoints

#### GET /api/status

Verifica que la API esté activa. No requiere autenticación.

```bash
curl http://tu-servidor:5001/api/status
```

Respuesta:

```json
{
  "status": "ok",
  "version": "1.0",
  "time_utc": "2026-04-25 14:00:00"
}
```

#### POST /api/qso

Registra un QSO para el operador indicado en `mycall`. El operador debe estar registrado en el sistema.

```bash
curl -X POST http://tu-servidor:5001/api/qso \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer HAMRADIOENCASTELLANO" \
  -d '{
    "call":      "K1ABC",
    "mycall":    "LU2FTI",
    "mode":      "FT8",
    "freq":      14.074,
    "extra":     "notas opcionales",
    "timestamp": "2026-04-25 14:00:00"
  }'
```

Campos del body:

| Campo     | Tipo   | Requerido | Descripcion                                      |
|-----------|--------|-----------|--------------------------------------------------|
| call      | string | Si        | Callsign del contacto                            |
| mycall    | string | Si        | Callsign del operador (debe estar registrado)    |
| mode      | string | No        | Modo de operacion: SSB, CW, FT8, FM, etc.       |
| freq      | number | No        | Frecuencia en MHz                                |
| extra     | string | No        | Notas adicionales                                |
| timestamp | string | No        | Fecha y hora UTC (formato: YYYY-MM-DD HH:MM:SS). Si se omite se usa la hora actual del servidor. |

Respuesta exitosa (`201`):

```json
{
  "status": "ok",
  "call": "K1ABC",
  "mode": "FT8",
  "mycall": "LU2FTI"
}
```

Errores posibles:

| Codigo | Descripción                                    |
|--------|------------------------------------------------|
| 400    | Body vacio, o falta el campo call o mycall     |
| 401    | Token de autorizacion ausente o incorrecto     |
| 403    | El mycall no esta registrado en el sistema     |

#### GET /api/qso

Lista todos los QSOs del operador autenticado via sesion web. Requiere estar logueado en la interfaz web (no usa el token de API).

```bash
curl -b cookies.txt http://tu-servidor:5001/api/qso
```

### Routing por mycall

El campo `mycall` determina en que archivo se guarda el QSO. El sistema construye la ruta `data/users/<MYCALL>/contacts.csv` y agrega el registro ahi. Cada operador registrado tiene su propio directorio y sus contactos son completamente independientes.

---

## Almacenamiento

### CSV (actual)

Los contactos se guardan en archivos CSV dentro de `data/users/<CALLSIGN>/contacts.csv`. Los usuarios se almacenan en `data/users.json` con las contraseñas hasheadas usando Werkzeug (pbkdf2:sha256).

La carpeta `data/` esta montada como volumen bind en Docker, por lo que los datos persisten en el sistema de archivos local del servidor y sobreviven a cualquier rebuild o recreacion de contenedores.

### SQLite (futuro)

La capa de storage esta abstraida en `storage/base.py`. Para migrar a SQLite basta con implementar `storage/sqlite_backend.py` con los mismos cinco metodos (`load_contacts`, `save_contacts`, `append_contact`, `delete_contact`, `update_contact`) y cambiar `STORAGE_BACKEND=sqlite` en el `.env`.

---

## Arquitectura de red

```
Internet
    |
   nginx (puerto 5001)
    |   proxy reverso, manejo de conexiones
    |
  Gunicorn (2 workers)
    |   servidor WSGI de produccion
    |
  Flask app
    |
  data/users/<CALLSIGN>/contacts.csv
```

nginx no maneja autenticacion — delega todo al login de Flask. Gunicorn corre con 2 workers, suficiente para uso personal o de un grupo reducido de operadores.

---

## Comandos útiles

```bash
# Levantar
docker compose up -d

# Ver logs de la app
docker logs minilog_app -f

# Ver logs de nginx
docker logs minilog_nginx -f

# Reconstruir imagen tras cambios de codigo
docker compose up -d --build

# Bajar sin borrar datos
docker compose down

# Ver archivos de datos
docker exec minilog_app find /app/data -type f

# Re build force - para que tome las variables del .env
docker compose up -d --force-recreate minilog
```

---

## Licencia

Proyecto libre para uso personal. Si lo usas o modificas, se agradece mencionarlo.
