# GatePass — Personnel Exit Pass & Fleet Control System

Sistema backend para automatizar el control de pases de salida de personal y la gestión de vehículos institucionales. Reemplaza el proceso manual de papeles firmados con un flujo digital de aprobaciones, trazabilidad completa de eventos y reportes narrativos automáticos generados por IA local.

---

## El Problema

En instituciones con salidas frecuentes de personal (hospitales, municipios, colegios, empresas), el proceso tradicional es:

- El empleado busca a su jefe para que firme un papel
- Luego va a RRHH a buscar otra firma
- Luego presenta el papel en garita
- El vigilante anota en un cuaderno
- Al final del mes, RRHH cuenta papeles a mano para generar reportes

**Resultado:** tiempo perdido, papeles extraviados, cero trazabilidad, reportes inexactos y empleados yendo de oficina en oficina preguntando si ya los aprobaron.

---

## La Solución

GatePass digitaliza todo el flujo:

1. Se genera un ticket de salida en el sistema
2. El empleado recibe un WhatsApp confirmando que su solicitud está en proceso
3. El jefe aprueba desde su panel web → WhatsApp al empleado
4. RRHH aprueba → WhatsApp al empleado con confirmación final
5. El vigilante marca la salida en garita
6. El conductor confirma los pasajeros
7. RRHH puede consultar reportes en cualquier momento por WhatsApp a la IA

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

## Levantar el proyecto

Ver [docs/setup.md](docs/setup.md)

---

## Base de datos

Ver diagrama completo en [docs/er_diagram.md](docs/er_diagram.md)

---

## Decisiones técnicas

Ver [docs/arquitectura.md](docs/arquitectura.md)
