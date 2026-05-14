# GatePass — Personnel Exit Pass & Fleet Control System

Sistema backend para automatizar el control de pases de salida de personal y la gestión de vehículos institucionales. Reemplaza el proceso manual de papeles firmados con un flujo digital de aprobaciones, trazabilidad completa de eventos y reportes narrativos automáticos generados por IA local.

---

## El Problema

En instituciones con salidas frecuentes de personal (hospitales, municipios, colegios, empresas), el proceso tradicional es:

- El empleado busca a su jefe para que firme un papel
- Luego va a RRHH a buscar otra firma
- Luego presenta el papel en garita
- El vigilante anota en un cuaderno
- Al final del mes, RRHH cuenta cada ticket uno por uno y elabora el reporte en Excel

**Resultado:** tiempo perdido, papeles extraviados, cero trazabilidad y reportes inexactos.

**Impacto económico:** El personal de RRHH dedica aproximadamente 1 hora diaria contando tickets uno por uno y elaborando reportes en Excel (6 días a la semana × 4 semanas = 24 horas al mes). Con un sueldo de $400 USD/mes, se estiman aproximadamente $60 USD mensuales desperdiciados en tiempo administrativo no productivo.

---

## La Solución

GatePass digitaliza todo el flujo:

1. Se genera un ticket de salida en el sistema
2. El empleado recibe un WhatsApp confirmando que su solicitud está en proceso
3. El jefe aprueba desde su panel web → WhatsApp al empleado
4. RRHH aprueba → WhatsApp al empleado con confirmación final
5. El vigilante marca la salida en garita
6. El conductor confirma los pasajeros
7. Ollama genera reportes automáticos diarios y semanales consolidados
8. RRHH puede consultar reportes en cualquier momento por WhatsApp a la IA

**Impacto:** Con reportes automáticos diarios y semanales generados por IA, la empresa ahorra aproximadamente $60 USD mensuales en tiempo administrativo no productivo.

---

## Flujo de un Ticket

```
Empleado solicita salida
        │
        ▼
Ticket creado → WhatsApp al empleado: "En proceso..."
        │
        ▼
Jefe aprueba → WhatsApp al empleado: "Aprobado por tu jefe..."
        │
        ▼
RRHH aprueba → WhatsApp al empleado: "✅ Listo, preséntate en garita"
        │
        ▼
Vigilante marca salida en garita
        │
        ▼
Conductor confirma pasajeros
        │
        ▼
Bitácora completa disponible para reportes
```

---

## Consultas e Informes por WhatsApp (IA)

RRHH puede escribirle directamente a Ollama por WhatsApp:

- *"¿Cuántas veces salió Juan Pérez esta semana?"*
- *"Reporte de salidas de hoy"* → responde con PDF
- *"¿Qué vehículos tienen el SOAT por vencer?"*

Ollama consulta la base de datos, genera una respuesta narrativa y la manda de vuelta por WhatsApp — en texto o como PDF según se pida.

---

## Stack

| Capa | Tecnología |
|------|------------|
| Framework | FastAPI |
| Base de datos | PostgreSQL |
| ORM | SQLAlchemy + Alembic |
| Autenticación | JWT (python-jose) |
| IA local | Ollama |
| Automatización | n8n |
| PDF | Jinja2 + WeasyPrint |
| Contenedores | Docker + Docker Compose |
| Frontend | React + Shadcn/ui |

---

## Roles del sistema

| Rol | Acceso |
|-----|--------|
| `superadmin` | Todo — usuarios, vehículos, configuración |
| `rrhh` | Aprobación de tickets + consultas a Ollama |
| `jefe_area` | Aprobación de tickets de su área |
| `conductor` | Ver sus asignaciones del día |
| `vigilante` | Marcar salida/retorno en garita |

---

## Estructura del proyecto

```
gatepass/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # endpoints por recurso
│   │   ├── core/           # config, db, jwt, roles
│   │   ├── models/         # tablas SQLAlchemy
│   │   ├── schemas/        # validación Pydantic
│   │   └── services/       # lógica de negocio, Ollama, WhatsApp
│   ├── migrations/         # historial de cambios de DB
│   └── tests/
├── frontend/               # React + Shadcn
├── n8n/workflows/          # automatizaciones WhatsApp
└── docs/                   # diagramas y documentación técnica
```

---

## Estado de Implementación

### Modelos (SQLAlchemy)
| Modelo | Tabla | Estado |
|--------|-------|--------|
| Rol | `roles` | ✅ Creado + seed fijo |
| Area | `areas` | ✅ Creado + seed fijo |
| Usuario | `usuarios` | ✅ Creado |
| CuentaAdmin | `cuentas_admin` | ✅ Creado |
| TipoVehiculo | `tipos_vehiculo` | ✅ Creado + seed fijo |
| Vehiculo | `vehiculos` | ✅ Creado + seed inicial |
| Conductor | `conductores` | ✅ Creado |
| AsignacionTransporte | `asignaciones_transporte` | ✅ Creado |
| TicketSalida | `tickets_salida` | ✅ Creado |
| BitacoraEvento | `bitacora_eventos` | ✅ Creado |

### Seeders (se ejecutan al iniciar la app)
| Seeder | Datos insertados |
|--------|-----------------|
| `seed_roles` | superadmin, rrhh, jefe_area, conductor, vigilante |
| `seed_areas` | Administración, RRHH, Logística, Operaciones, Gerencia |
| `seed_superadmin` | Cuenta admin inicial (desde variables de entorno) |
| `seed_tipos_vehiculo` | Sedan, SUV, Camioneta, Van, Bus |
| `seed_vehiculos` | 7 vehículos de ejemplo |

### Endpoints de la API (`/api/v1`)
| Recurso | GET | POST | PUT | DELETE | Auth |
|---------|-----|------|-----|--------|------|
| `/auth/login` | — | ✅ Login | — | — | Público |
| `/auth/cuenta` | — | ✅ Crear cuenta admin | — | — | superadmin |
| `/auth/me` | ✅ Perfil actual | — | — | — | Cualquiera |
| `/usuarios/areas` | ✅ Listar | ✅ Crear | ✅ Editar | ✅ Eliminar | GET: auth, resto: superadmin |
| `/roles` | ✅ Listar | — | — | — | Cualquiera autenticado |
| `/tipos-vehiculo` | ✅ Listar | ✅ Crear | ✅ Editar | ✅ Eliminar | GET: auth, resto: superadmin |
| `/vehiculos` | ✅ Listar | ✅ Crear | ✅ Editar | ✅ Eliminar | GET: auth, resto: superadmin |

### Próximos endpoints (pendientes)
- Usuario CRUD
- Conductor CRUD
- AsignacionTransporte CRUD
- TicketSalida CRUD + flujo de aprobaciones
- BitacoraEvento endpoints
- Reportes con IA (Ollama)

---

## Levantar el proyecto

Ver [docs/setup.md](docs/setup.md)

---

## Base de datos

Ver diagrama completo en [docs/er_diagram.md](docs/er_diagram.md)

---

## Decisiones técnicas

Ver [docs/arquitectura.md](docs/arquitectura.md)
