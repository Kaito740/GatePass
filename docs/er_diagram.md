# Diagrama de Base de Datos — GatePass

```mermaid
erDiagram

    %% --- IDENTIDAD Y ACCESO ---

    roles {
        int id PK
        varchar nombre
    }

    areas {
        int id PK
        varchar nombre
    }

    usuarios {
        int id PK
        varchar dni UK
        varchar nombres
        varchar apellidos
        int rol_id FK
        varchar cargo
        int area_id FK
        varchar telefono_wa UK
        boolean activo
        timestamp created_at
    }

    cuentas_admin {
        int id PK
        int usuario_id FK
        varchar password_hash
    }

    %% --- LOGÍSTICA ---

    tipos_vehiculo {
        int id PK
        varchar nombre
    }

    vehiculos {
        int id PK
        varchar placa UK
        int tipo_id FK
        int capacidad_pasajeros
        varchar marca
        varchar modelo
        int año
        varchar color
        date soat_vencimiento
        varchar estado_actual
        boolean activo
    }

    conductores {
        int id PK
        int usuario_id FK
        varchar licencia_categoria
        varchar licencia_numero
        date licencia_vencimiento
    }

    asignaciones_transporte {
        int id PK
        int conductor_id FK
        int vehiculo_id FK
        date fecha
        time hora_salida
        boolean is_active
    }

    %% --- OPERACIONES ---

    tickets_salida {
        int id PK
        int solicitante_id FK
        int aprobador_jefe_id FK
        int aprobador_rrhh_id FK
        int asignacion_id FK
        varchar destino
        text motivo
        varchar status
        timestamp created_at
    }

    bitacora_eventos {
        int id PK
        int ticket_id FK
        int registrado_por FK
        varchar tipo_accion
        timestamp fecha_hora
    }

    %% --- RELACIONES ---

    roles        ||--o{ usuarios              : "tiene"
    areas        ||--o{ usuarios              : "pertenece"
    usuarios     ||--o| cuentas_admin         : "tiene cuenta"
    usuarios     ||--o| conductores           : "es conductor"
    tipos_vehiculo ||--o{ vehiculos           : "clasifica"
    conductores  ||--o{ asignaciones_transporte : "asignado a"
    vehiculos    ||--o{ asignaciones_transporte : "usado en"
    asignaciones_transporte ||--o{ tickets_salida : "cubre"
    usuarios     ||--o{ tickets_salida        : "solicita"
    usuarios     ||--o{ tickets_salida        : "aprueba jefe"
    usuarios     ||--o{ tickets_salida        : "aprueba rrhh"
    tickets_salida ||--o{ bitacora_eventos    : "registra"
    usuarios     ||--o{ bitacora_eventos      : "registrado por"
```

---

## Notas importantes

### Roles — datos semilla, sin POST público
Los roles viajan con la DB al arrancar. No hay endpoint para crearlos desde fuera.

| ID | Rol |
|----|-----|
| 1 | superadmin |
| 2 | rrhh |
| 3 | jefe_area |
| 4 | conductor |
| 5 | vigilante |

### `status` en tickets_salida
Valores permitidos:

| Estado | Descripción |
|--------|-------------|
| `pendiente` | Recién creado, esperando jefe |
| `aprobado_jefe` | Jefe aprobó, esperando RRHH |
| `aprobado_rrhh` | Completamente aprobado |
| `rechazado` | Rechazado en cualquier etapa |
| `activo` | Empleado ya salió |
| `cerrado` | Retornó |

### `tipo_accion` en bitacora_eventos
Valores permitidos:

| Acción | Quién la registra |
|--------|------------------|
| `salida_garita` | Vigilante |
| `retorno_garita` | Vigilante |
| `abordaje_vehiculo` | Conductor |

### `soat_vencimiento` en vehiculos
Campo crítico — n8n revisa este campo y dispara alerta por WhatsApp cuando faltan 30 días para el vencimiento.
