<div align="center">
  <h1>Diana Nails · Smart Booking</h1>
  <p>
    <strong>Sistema Inteligente de Agendamiento con Recordatorios WhatsApp<br>
    y Analítica Basada en Matemáticas Discretas</strong>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white">
    <img src="https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white">
    <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white">
    <img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white">
    <img src="https://img.shields.io/badge/NetworkX-3.4-FF6F00?logo=python&logoColor=white">
    <img src="https://img.shields.io/badge/SciPy-1.14-8CAAE6?logo=scipy&logoColor=white">
    <img src="https://img.shields.io/badge/WhatsApp-Cloud_API-25D366?logo=whatsapp&logoColor=white">
    <img src="https://img.shields.io/badge/license-MIT-green">
  </p>
</div>

---

## Tabla de Contenidos

1. [Descripción](#descripción)
2. [Tecnologías](#tecnologías)
3. [Arquitectura](#arquitectura)
4. [Modelo de Datos](#modelo-de-datos)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Funcionalidades](#funcionalidades)
7. [Módulo de Matemáticas Discretas](#módulo-de-matemáticas-discretas)
8. [Sistema de Notificaciones WhatsApp](#sistema-de-notificaciones-whatsapp)
9. [Instalación](#instalación)
10. [Configuración](#configuración)
11. [Variables de Entorno](#variables-de-entorno)
12. [Uso](#uso)
13. [Futuras Mejoras](#futuras-mejoras)
14. [Licencia](#licencia)

---

## Descripción

**Diana Nails Smart Booking** es un sistema integral de gestión de citas diseñado para el spa **Diana Nails**. Combina un backend robusto en Django con técnicas de **matemáticas discretas** —teoría de grafos, combinatoria, lógica proposicional y distribución binomial— para optimizar la agenda, predecir cancelaciones y generar recomendaciones inteligentes.

El sistema incluye recordatorios automáticos por WhatsApp mediante una arquitectura extensible de proveedores (Meta Cloud API y Twilio), panel administrativo responsivo con temática spa, y un módulo independiente de analítica cuantitativa.

### ¿Por qué Matemáticas Discretas?

La gestión de citas en un spa presenta problemas que se modelan naturalmente con matemáticas discretas:

| Problema | Modelo Matemático | Aplicación |
|----------|-------------------|------------|
| ¿Qué servicios se toman juntos? | Grafo bipartito clientes-servicios | Recomendaciones colaborativas |
| ¿Hay conflictos de horario? | Grafo de intervalos (intersección) | Detección O(n log n) de solapamientos |
| ¿Cuántos paquetes de servicios ofrecer? | Combinaciones C(n,k) | Creación de paquetes promocionales |
| ¿De cuántas formas ordenar las citas? | Permutaciones P(n,k) | Optimización de agenda |
| ¿Es válida esta cita? | Lógica proposicional (∧, →, ¬) | Motor de restricciones de negocio |
| ¿Cuántas cancelaciones esperar? | Distribución Binomial B(n,p) | Overbooking y predicción |

---

## Tecnologías

### Core
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.12+ | Lenguaje base |
| Django | 5.1.4 | Framework web full-stack |
| PostgreSQL | 16+ | Base de datos relacional |
| Gunicorn | 23.0 | Servidor WSGI de producción |
| Whitenoise | 6.8 | Servicio de estáticos en producción |

### Frontend
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Bootstrap | 5.3 | Framework CSS responsivo |
| Chart.js | 4.x | Gráficos del dashboard |
| Bootstrap Icons | 1.x | Iconografía |
| Google Fonts (Inter) | — | Tipografía principal |

### Analítica & Matemáticas
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| NetworkX | 3.4.2 | Teoría de grafos |
| SciPy | 1.14.1 | Distribuciones estadísticas |
| Matplotlib | 3.9.3 | Visualización de grafos y distribuciones |
| NumPy | 2.1.3 | Cómputo numérico |
| Pandas | 2.2.3 | Manipulación de datos |

### Notificaciones
| Tecnología | Propósito |
|------------|-----------|
| Meta WhatsApp Cloud API v21.0 | Proveedor principal de WhatsApp |
| Twilio WhatsApp API | Proveedor alternativo |
| `requests` 2.32 | HTTP client para ambas APIs |

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                            DJANGO                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │  Core     │ │ Accounts │ │ Clients  │ │ Services │ │Specialists│ │
│  │(mixins,   │ │(auth,    │ │(CRUD,    │ │(catálogo,│ │(perfiles, │ │
│  │ enums,    │ │ perfiles)│ │ historial)│ │tipos de  │ │servicios) │ │
│  │ modelos   │ │          │ │          │ │ uñas)    │ │           │ │
│  │ base)     │ │          │ │          │ │          │ │           │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────────┐  │
│  │ Schedules│ │Appointment│ │Notific. │ │     Analytics        │  │
│  │(horarios,│ │(citas,   │ │(WhatsApp,│ │  (estadísticas,      │  │
│  │ descansos│ │validación│ │plantillas│ │   reportes)           │  │
│  │, días    │ │, estados)│ │, program.│ │                      │  │
│  │ libres)  │ │          │ │ )        │ │                      │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────────┘  │
│                          │                                         │
│                          ▼                                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              MATEMÁTICAS DISCRETAS (self-contained)          │  │
│  │  ┌─────────┐ ┌──────────────┐ ┌──────────┐ ┌───────────┐  │  │
│  │  │ Grafos  │ │ Combinatoria │ │Lógica    │ │ Binomial  │  │  │
│  │  │(bipart.,│ │ (C(n,k),     │ │Prop.     │ │ (PMF, CDF,│  │  │
│  │  │conflic.,│ │ P(n,k))      │ │(∧,→,¬)   │ │ E[X],     │  │  │
│  │  │ BFS/DFS)│ │              │ │          │ │overbooking│  │  │
│  │  └─────────┘ └──────────────┘ └──────────┘ └───────────┘  │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
         │                                    │
         ▼                                    ▼
┌──────────────────┐          ┌──────────────────────────┐
│   PostgreSQL     │          │   WhatsApp Provider      │
│   (14 tablas)    │          │  ┌──────┐  ┌──────────┐ │
│                  │          │  │ Meta │  │ Twilio   │ │
│                  │          │  │Cloud │  │ WhatsApp │ │
│                  │          │  │ API  │  │ API      │ │
│                  │          │  └──────┘  └──────────┘ │
└──────────────────┘          └──────────────────────────┘
```

### Patrones de Diseño Implementados

| Patrón | Ubicación | Descripción |
|--------|-----------|-------------|
| **Strategy** | `notifications/services/` | Proveedores WhatsApp intercambiables (Meta/Twilio) |
| **Factory** | `provider_factory.py` | Selección dinámica del proveedor vía `WHATSAPP_PROVIDER` |
| **Template Method** | `BaseModel.save()` → `clean()` | Validación antes de guardar |
| **Mixin** | `core/models.py` | `UUIDModel`, `TimeStampedModel`, `SoftDeleteModel` combinados en `BaseModel` |
| **Domain Model** | `Appointment.reschedule()` | Lógica de negocio encapsulada en el modelo |
| **Singleton** | `notifications/services/__init__.py` | Instancia única del servicio de notificaciones |
| **Observer** | `signals.py` | Disparo automático de notificaciones al cambiar estado de cita |

---

## Modelo de Datos

### Base Models (abstractos, todas las tablas heredan de `BaseModel`)

```
UUIDModel         TimeStampedModel      SoftDeleteModel
    │                   │                    │
    └───────────────────┴────────────────────┘
                        │
                    BaseModel
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    Client        Appointment      Specialist
    Service        Schedule         NotificationLog
    ...
```

- **`UUIDModel`**: `id` UUID como PK (no auto-incremental, seguro, escalable)
- **`TimeStampedModel`**: `created_at`, `updated_at` automáticos
- **`SoftDeleteModel`**: `is_active` + `deleted_at` — borrado lógico con `soft_delete()`/`restore()`
- **`BaseModel`**: Los tres anteriores combinados

### Diagrama Entidad-Relación

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│    Client    │─────│   Appointment    │─────│  Specialist  │
│ (clientas)   │     │     (citas)      │     │(especialistas)│
└──────────────┘     │                  │     └──────────────┘
                     │ status:          │           │
┌──────────────┐     │  pending         │           │
│   Service    │─────│  confirmed       │     ┌──────────────┐
│ (servicios)  │     │  in_progress     │─────│ WorkSchedule │
│              │     │  completed       │     │  (horarios)  │
│ category:    │     │  cancelled       │     └──────────────┘
│  nail        │     │  no_show         │           │
│  eyebrow     │     │                  │     ┌──────────────┐
│  waxing      │     │ rescheduled_from─│─self│   DayOff     │
│  other       │     │ (self FK)        │     │ (días libres)│
└──────────────┘     └────────┬─────────┘     └──────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ NotificationLog  │
                    │ (whatsapp/sms)   │
                    │ status:          │
                    │  pending/sent/   │
                    │  failed          │
                    │ provider:        │
                    │  meta/twilio     │
                    └──────────────────┘
```

### Enumeraciones (TextChoices / IntegerChoices)

| Enum | Valores |
|------|---------|
| `BusinessDayChoices` | LUNES(0) – SÁBADO(5) |
| `AppointmentStatus` | pending, confirmed, in_progress, completed, cancelled, no_show |
| `NotificationType` | reminder, confirmation, cancellation, follow_up |
| `NotificationStatus` | pending, sent, failed |
| `ServiceMainCategory` | nail, eyebrow, waxing, other |

---

## Estructura del Proyecto

```
diana-nails-smart-booking/
│
├── config/                          # Configuración de Django
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py                  # Configuración base
│   │   ├── development.py           # Debug, toolbar, consola email
│   │   └── production.py            # HSTS, SSL, logging
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py                      # 9 namespaces de apps
│   └── wsgi.py
│
├── apps/                            # Aplicaciones modulares
│   ├── core/                        # Modelos base, enums, context processors
│   │   └── models.py
│   ├── accounts/                    # Auth, UserProfile
│   ├── clients/                     # CRUD clientas, historial
│   ├── services/                    # Catálogo, categorías, tipos de uñas
│   ├── specialists/                 # Especialistas, servicios asociados
│   ├── schedules/                   # WorkSchedule, BreakSchedule, DayOff
│   │   └── services/
│   │       └── availability.py      # Algoritmo de slots disponibles
│   ├── appointments/                # Citas, validaciones, reschedule
│   ├── notifications/               # WhatsApp, plantillas, scheduling
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # Provider ABC
│   │   │   ├── provider_factory.py  # Factory (Meta/Twilio)
│   │   │   ├── meta_provider.py     # Meta Cloud API
│   │   │   ├── twilio_provider.py   # Twilio API
│   │   │   ├── notification_service.py  # Orchestrador
│   │   │   ├── scheduler.py         # Programador de recordatorios
│   │   │   └── message_templates.py # Plantillas de mensajes
│   │   ├── signals.py               # Auto-disparo de notificaciones
│   │   └── management/commands/
│   │       └── process_notifications.py  # Cron command
│   └── analytics/                   # DailySummary, CancellationStat, ServiceStat
│
├── mathematics/                     # Módulo independiente de matemáticas
│   ├── graphs/                      # Teoría de grafos (NetworkX)
│   │   ├── client_service_graph.py  # Grafo bipartito clientes-servicios
│   │   ├── schedule_graph.py        # Grafo dirigido de slots
│   │   ├── conflict_graph.py        # Grafo de intervalos (conflictos)
│   │   └── traversal.py             # BFS, DFS, componentes conexas
│   ├── combinatorics/               # Combinatoria aplicada
│   │   ├── service_combinations.py  # C(n,k), paquetes, duraciones
│   │   └── schedule_arrangements.py # P(n,k), palomar, conflictos
│   ├── discrete_logic/              # Lógica proposicional
│   │   ├── constraints.py           # Validador con ∧ proposicional
│   │   ├── business_rules.py        # Reglas antecedente → consecuente
│   │   └── conflict_detector.py     # Detección O(n²) de solapamientos
│   ├── binomial/                    # Distribución binomial
│   │   ├── cancellation_analysis.py # PMF, CDF, E[X], Var, overbooking
│   │   └── cancellation_predictor.py# Escenarios, mejora de proceso
│   ├── visualizations/              # matplotlib + networkx
│   │   ├── graph_plotter.py         # Gráficos de grafos
│   │   └── stats_plotter.py         # Gráficos de distribuciones
│   └── run_examples.py              # Script que ejecuta todo
│
├── templates/                       # Django Templates (Bootstrap 5)
│   ├── base.html                    # Layout con sidebar + navbar
│   ├── dashboard.html               # Dashboard con Chart.js
│   ├── components/                  # Navbar, sidebar, footer, paginación
│   │   ├── navbar.html              #   breadcrumb, stat_card, modal
│   │   ├── sidebar.html             #   page_header
│   │   └── ...
│   ├── accounts/login.html
│   ├── clients/                     # List, form, delete
│   ├── services/                    # Servicios, categorías, tipos de uñas
│   ├── specialists/
│   ├── schedules/                   # Horarios, descansos, días libres
│   ├── appointments/                # CRUD + cancelación
│   ├── notifications/
│   └── analytics/
│
├── static/                          # Archivos estáticos
│   ├── css/
│   │   ├── style.css                # Tema spa (742 líneas)
│   │   └── admin-custom.css         # Estilo admin
│   ├── js/
│   │   ├── main.js                  # Sidebar toggle, alerts, tooltips
│   │   ├── appointments.js          # Cálculo automático de end_time
│   │   └── dashboard.js             # Gráfico Chart.js semanal
│   └── img/
│
├── scripts/                         # Scripts de automatización
│   ├── seed_data.py
│   ├── create_superuser.py
│   └── setup.sh
│
├── media/                           # Uploads
├── .env.example                     # Template de variables de entorno
├── .gitignore
├── manage.py
├── requirements.txt                 # 18 dependencias
└── README.md
```

---

## Funcionalidades

### Gestión de Citas
- CRUD completo de clientas, servicios, especialistas y citas
- Estados de cita: pendiente, confirmada, en proceso, completada, cancelada, inasistencia
- Reprogramación con trazabilidad (`rescheduled_from` + `AppointmentRescheduleLog`)
- Validaciones automáticas: horario laboral, duración máxima, sin conflictos, fecha futura
- Algoritmo de slots disponibles por especialista, fecha y duración
- Bloque de dos turnos: mañana (8:00–12:00) y tarde (13:00–20:00)

### Dashboard Administrativo
- Resumen con tarjetas estadísticas (citas hoy, cancelaciones, ingresos)
- Gráfico de citas semanales con Chart.js
- Paleta de colores spa: morado (#8B5E83), verde salvia (#5E8B6E), dorado (#E8C35E)
- Sidebar responsivo con secciones colapsables

### Sistema de Notificaciones WhatsApp
- Dos proveedores intercambiables: Meta Cloud API y Twilio
- 5 plantillas de mensajes: recordatorio (24h y 2h), confirmación, cancelación, seguimiento, reprogramación
- Programación automática vía `signals.py` al cambiar estado de cita
- Comando `process_notifications` para ejecución por cron
- Reintentos con backoff (máx. 3 intentos)
- Historial completo en `NotificationLog`

### Módulo de Matemáticas Discretas
Ver sección dedicada abajo.

---

## Módulo de Matemáticas Discretas

El módulo `mathematics/` es **completamente independiente de Django** — no tiene dependencias del ORM ni de los modelos. Opera con datos en memoria (listas, diccionarios) para ser testeable y reutilizable.

### Grafos (`mathematics/graphs/`)

#### ClientServiceGraph (Grafo Bipartito)
Modela la relación entre clientas y servicios. Las aristas conectan a cada clienta con los servicios que ha tomado.

```
     Clientes                    Servicios
    ┌──────┐                   ┌──────────┐
    │ Ana  │────Manicura──────▶│Manicura  │
    │      │────Pedicura──────▶│Pedicura  │
    │      │────Cejas─────────▶│Cejas     │
    ├──────┤                   ├──────────┤
    │ Betty│────Acrílicas─────▶│Acrílicas │
    │      │────Pedicura──────▶│Pestañas  │
    │      │────Masaje────────▶│Masaje    │
    └──────┘                   └──────────┘
```

**Algoritmo**: Recomendación colaborativa — si las clientas A y B comparten servicios, recomendar a A los servicios que B ha tomado y A no.

**Aplicación**: Sugerir servicios complementarios ("otras clientas que tomaron Manicura también tomaron Masaje").

#### ConflictGraph (Grafo de Intervalos)
Cada cita es un intervalo `[start_i, end_i)`. Hay una arista entre dos citas si sus intervalos se solapan.

```
Intervalos:                    Grafo de conflictos:
9:00  10:00  11:00  12:00
├─────┤                       A001 ─── A002
  ├─────┤                       │        │
    ├─────┤                     A003 ────┘
        ├─────┤                 │
            ├─────┤            A004 ─── A005
```

**Propiedad**: Número cromático = máximo de citas simultáneas. En O(n log n) con sweep-line.

**Aplicación**: Detectar si es viable agregar una cita; encontrar el momento del día más congestionado.

#### GraphTraversal (BFS / DFS)
- **BFS**: Distancia más corta entre dos clientas en el grafo bipartito (camino clienta → servicio → clienta)
- **DFS**: Exploración completa del grafo desde un nodo
- **Componentes conexas**: Grupos de clientas que comparten servicios indirectamente

### Combinatoria (`mathematics/combinatorics/`)

#### ServiceCombinations
| Fórmula | Cálculo | Aplicación |
|---------|---------|------------|
| C(n,k) = n! / (k!(n-k)!) | Combinaciones de k servicios | Paquetes promocionales |
| P(n,k) = n! / (n-k)! | Permutaciones de k servicios | Orden de atención |
| Σ C(n,k) | Todos los paquetes posibles | Estrategia de precios |
| n^k | Secuencias con repetición | Secuencias de servicios en un día |

Ejemplo con 10 servicios:
- C(10,2) = **45** paquetes de 2 servicios
- C(10,3) = **120** paquetes de 3 servicios
- Total paquetes posibles = **1023**

#### ScheduleArrangements
- **Principio del palomar**: si hay más citas que slots, al menos un slot tiene 2+ citas
- **Probabilidad de conflicto**: `1 - P(n,k) / n^k` — con 16 slots y 5 citas, la probabilidad de que la asignación aleatoria genere conflictos es **99.8%**
- **Factorial growth**: 10! = 3.6 millones, 15! = 1.3 billones — por qué la búsqueda exhaustiva es inviable

### Lógica Discreta (`mathematics/discrete_logic/`)

#### ConstraintValidator (Lógica Proposicional)
Una cita es válida **si y solo si** todas las restricciones se cumplen:

```
Válida = C₁ ∧ C₂ ∧ C₃ ∧ ... ∧ Cₙ
```

Donde cada Cᵢ es una proposición como:
- C₁: Horario laboral `(hora ≥ 8:00 ∧ hora < 12:00) ∨ (hora ≥ 13:00 ∧ hora < 20:00)`
- C₂: ¬Conflicto `¬(start_i < end_j ∧ start_j < end_i)`
- C₃: ¬Día libre
- C₄: Duración ≤ 180 min
- C₅: Fecha futura
- C₆: Anticipación ≥ 2h

#### BusinessRules
Reglas de negocio como implicaciones: **antecedente → consecuente**

| Regla | Antecedente | Consecuente |
|-------|-------------|-------------|
| Tipo de uñas | Servicio es nail | Tipo de aplicación especificado |
| Horario | Cita en la mañana | End ≤ 12:00 |
| Anticipación | Cita creada | Fecha ≥ hoy + 2h |
| Sin doble agenda | Especialista asignado | Sin conflicto con otras citas |

**Tabla de verdad**: genera 2ⁿ filas para n variables, verificando tautologías.

### Distribución Binomial (`mathematics/binomial/`)

Modela las cancelaciones como experimentos de Bernoulli: cada cita es un ensayo con probabilidad p de cancelación.

```
X ~ Binomial(n, p)
P(X = k) = C(n,k) · p^k · (1-p)^(n-k)
```

| Estadístico | Fórmula | Ejemplo (n=100, p=0.15) |
|-------------|---------|--------------------------|
| Esperanza | E[X] = np | 15.0 cancelaciones |
| Varianza | Var(X) = np(1-p) | 12.75 |
| Desv. estándar | σ = √Var | 3.57 |
| Sesgo | (1-2p)/σ | 0.196 (cola derecha) |
| Moda | ⌊(n+1)p⌋ | 15 cancelaciones |
| P(X=0) | (1-p)ⁿ | 0.00000001 |

#### Overbooking Inteligente
Dados 20 slots disponibles y una tasa de cancelación del 15%:
- 1 extra: riesgo del **1.7%** de que vengan más de 20 clientas
- 3 extras: riesgo del **21.7%**
- **Óptimo**: 2 extras (riesgo < 10%)

---

## Sistema de Notificaciones WhatsApp

### Arquitectura de Proveedores

```
                    ┌──────────────────────┐
                    │   NotificationService │  ← Orchestrador
                    └──────┬───────────────┘
                           │
                    ┌──────▼───────────────┐
                    │   ProviderFactory    │  ← Selecciona vía env var
                    │  .get_provider()     │
                    └──────┬───────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
    ┌──────────────┐ ┌──────────┐ ┌──────────┐
    │     Meta     │ │  Twilio  │ │ Futuros  │
    │ WhatsApp    │ │ WhatsApp │ │ (WATI,   │
    │ Cloud API   │ │ API      │ │ 360dialog)│
    └──────────────┘ └──────────┘ └──────────┘
```

### Flujo de una Notificación

```
1. Appointment.save() → señal post_save
2. NotificationScheduler.schedule_reminders()
   → Crea 2 NotificationLog (24h antes, 2h antes)
3. Cron (cada 5 min):
   python manage.py process_notifications
4. NotificationService.process_pending()
5. ProviderFactory.get_provider('meta').send_message()
6. NotificationLog.mark_as_sent(failed)
```

### Plantillas de Mensajes

| Tipo | Cuándo se envía | Ejemplo |
|------|-----------------|---------|
| Recordatorio 24h | 24h antes de la cita | "💅 Recordatorio: mañana a las 15:00 tienes Manicura con Diana" |
| Recordatorio 2h | 2h antes | "⏰ Tu cita es en 2 horas" |
| Confirmación | Al crear/confirmar | "✅ Cita confirmada para el lunes 10:00" |
| Cancelación | Al cancelar | "❌ Tu cita del lunes 10:00 ha sido cancelada" |
| Seguimiento | Día después de completar | "📝 ¿Cómo fue tu experiencia?" |

---

## Instalación

### Requisitos

- Python 3.12 o superior
- PostgreSQL 16 o superior
- Git

### Paso a Paso

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/diana-nails-smart-booking.git
cd diana-nails-smart-booking

# 2. Crear y activar entorno virtual
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS / Linux:
# source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales (ver sección Variables de Entorno)

# 5. Crear la base de datos PostgreSQL
psql -U postgres
CREATE DATABASE diana_nails_booking;
\q

# 6. Ejecutar migraciones
python manage.py migrate

# 7. Crear superusuario
python manage.py shell < scripts/create_superuser.py

# (Opcional) Cargar datos de prueba
python manage.py shell < scripts/seed_data.py

# 8. Iniciar servidor de desarrollo
python manage.py runserver

# 9. Visitar http://127.0.0.1:8000/
```

### Ejecutar Módulo de Matemáticas

```bash
# El módulo matemáticas NO requiere Django
python mathematics/run_examples.py
```

Si matplotlib está instalado, generará gráficos en `mathematics/output/`.

### Configurar Notificaciones

```bash
# Procesar notificaciones pendientes (ideal para cron cada 5 min)
python manage.py process_notifications --retry --max 50 --verbose

# Simulación (no envía realmente)
python manage.py process_notifications --dry-run --verbose
```

---

## Configuración

### Entornos

| Archivo | Propósito |
|---------|-----------|
| `config/settings/base.py` | Configuración común a todos los entornos |
| `config/settings/development.py` | Desarrollo local: DEBUG=True, debug toolbar, consola email |
| `config/settings/production.py` | Producción: HSTS, SSL, logging a archivo, DEBUG=False |

### Cambiar entre entornos

El entorno se selecciona vía la variable `DJANGO_SETTINGS_MODULE` en `.env`:

```ini
# Desarrollo
DJANGO_SETTINGS_MODULE=config.settings.development

# Producción
# DJANGO_SETTINGS_MODULE=config.settings.production
```

### Proveedor WhatsApp

Seleccionar entre Meta y Twilio:

```ini
WHATSAPP_PROVIDER=meta    # Meta Cloud API (default)
# WHATSAPP_PROVIDER=twilio  # Twilio WhatsApp API
```

---

## Variables de Entorno

Todas las configuraciones sensibles se manejan via `.env`. Copiar `.env.example` a `.env`:

```ini
# ── Django ───────────────────────────────────────
DJANGO_SETTINGS_MODULE=config.settings.development
DJANGO_SECRET_KEY=tu-secret-key-aqui
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# ── PostgreSQL ───────────────────────────────────
DB_ENGINE=django.db.backends.postgresql
DB_NAME=diana_nails_booking
DB_USER=postgres
DB_PASSWORD=tu-password
DB_HOST=localhost
DB_PORT=5432

# ── Admin (setup inicial) ────────────────────────
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@diananails.com
ADMIN_PASSWORD=admin123

# ── WhatsApp Provider ────────────────────────────
WHATSAPP_PROVIDER=meta          # meta | twilio

# Meta WhatsApp Cloud API
WHATSAPP_API_URL=https://graph.facebook.com/v21.0
WHATSAPP_API_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_BUSINESS_PHONE=

# Twilio WhatsApp API
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# ── Notification Timing ─────────────────────────
NOTIFICATION_REMINDER_HOURS=24,2    # 24h y 2h antes

# ── Timezone ────────────────────────────────────
TZ=America/Bogota
```

> **⚠️ Seguridad**: Nunca commitees el archivo `.env` al repositorio. Está incluído en `.gitignore`.

---

## Uso

### Administración

```
/admin/    → Panel de administración de Django
/accounts/ → Login de usuarios
```

### Módulos Principales

| Ruta | Propósito |
|------|-----------|
| `/` | Dashboard con gráfico semanal |
| `/clients/` | Gestión de clientas (CRUD) |
| `/services/` | Catálogo de servicios, categorías, tipos de aplicación |
| `/specialists/` | Perfiles de especialistas |
| `/schedules/` | Horarios laborales, descansos, días libres |
| `/appointments/` | Agendamiento y gestión de citas |
| `/notifications/` | Historial de notificaciones enviadas |
| `/analytics/` | Estadísticas, cancelaciones, reportes |

### Commandos Útiles

```bash
# Procesar notificaciones (ejecutar cada 5-15 min via cron)
python manage.py process_notifications --retry --max 50

# Simular notificaciones
python manage.py process_notifications --dry-run --verbose

# Abrir shell con todos los modelos cargados
python manage.py shell_plus

# Seed data de prueba
python manage.py shell < scripts/seed_data.py

# Ejecutar ejemplos de matemáticas discretas
python mathematics/run_examples.py
```

---

## Futuras Mejoras

### Corto Plazo
- [ ] **Multi-especialista**: Permitir que varias especialistas tengan horarios independientes y citas paralelas
- [ ] **Pagos integrados**: Conexión con pasarela de pagos (anticipe o pago completo desde WhatsApp)
- [ ] **Panel de clienta**: Portal donde las clientas puedan ver su historial y agendar desde su celular

### Mediano Plazo
- [ ] **Árboles de decisión**: Predecir cancelaciones basado en variables (día de semana, hora, cliente recurrente)
- [ ] **Optimización por programación lineal**: Asignar slots óptimos maximizando ingresos y minimizando tiempos muertos
- [ ] **Clustering de clientas**: Segmentar clientas por comportamiento (frecuencia, servicios preferidos, sensibilidad a cancelación) usando k-means
- [ ] **Reportes exportables**: Descargar estadísticas en PDF/Excel

### Largo Plazo
- [ ] **Aplicación móvil**: App para clientas con agendamiento, notificaciones push e historial
- [ ] **Machine Learning**: Predicción de demanda para optimizar horarios de la especialista día a día
- [ ] **Integración con calendarios**: Google Calendar / iCal sincronización bidireccional
- [ ] **Multi-sede**: Soporte para múltiples sucursales con inventario y especialistas independientes

---

## Licencia

Distribuido bajo licencia MIT. Ver `LICENSE` para más información.

---

<div align="center">
  <sub>Desarrollado para <strong>Diana Nails Spa</strong> — 2026</sub>
  <br>
  <sub>Curso de Matemáticas Discretas · 3<sup>er</sup> Corte</sub>
</div>
