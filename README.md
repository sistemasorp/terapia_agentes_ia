# 🧠 Multi-Agent AI — Simulación de interacción psicológica

**Prueba de concepto de un sistema multiagente desarrollado con OpenAI Agents SDK, Python y SQLite.**

Este proyecto explora cómo varios agentes de inteligencia artificial pueden interactuar de forma autónoma, mantener memoria conversacional persistente y evaluar sus propias interacciones dentro de un escenario simulado.

Para ello, se ha elegido una conversación ficticia entre un profesional de la psicología y una persona que presenta síntomas compatibles con un cuadro depresivo.

> **Aviso importante:** Este proyecto tiene una finalidad exclusivamente tecnológica, experimental y educativa. No constituye una herramienta de diagnóstico, tratamiento o intervención psicológica, ni pretende reproducir o sustituir el trabajo de profesionales de la salud mental.

## 🎯 Objetivos

El propósito de esta prueba de concepto es investigar distintas capacidades de los sistemas multiagente:

- Comunicación autónoma entre agentes especializados.
- Persistencia de memoria entre ejecuciones.
- Mantenimiento de roles y contextos independientes.
- Evaluación automatizada de intervenciones mediante otro agente.
- Representación de estados internos mediante variables cuantificables.
- Evolución de variables sintéticas a través de reglas programadas.
- Registro de resultados para su posterior análisis.

El objetivo no es evaluar la eficacia de una terapia, sino estudiar el comportamiento y las limitaciones de una arquitectura multiagente.

## 🏗️ Arquitectura

El sistema está formado por tres agentes desarrollados mediante OpenAI Agents SDK.

### 1. Agente Psicólogo

Simula un interlocutor que utiliza estrategias comunicativas inspiradas en la escucha activa y la terapia cognitivo-conductual.

Sus instrucciones incluyen formular preguntas abiertas, mantener una comunicación respetuosa y evitar diagnósticos o recomendaciones médicas.

### 2. Agente Paciente

Interpreta a Marcos, un personaje ficticio de 35 años que presenta síntomas como tristeza persistente, apatía, problemas de sueño, cansancio y aislamiento social.

El personaje mantiene una historia predefinida y dispone de memoria conversacional para conservar la continuidad entre intervenciones.

### 3. Agente Evaluador

Analiza las intervenciones generadas por el agente Psicólogo y devuelve una evaluación estructurada de tres características comunicativas:

- Empatía expresada.
- Escucha y atención al contenido.
- Presión comunicativa.

Estas valoraciones son generadas por un modelo de lenguaje y no representan evaluaciones clínicas validadas.

### Flujo de ejecución

```text
                 ┌────────────────────┐
                 │ Controlador Python │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ Agente Psicólogo   │
                 └─────────┬──────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
             ┌────────────┐ ┌────────────┐
             │ Evaluador  │ │ Evolución  │
             │ de diálogo │ │ de estado  │
             └──────┬─────┘ └──────┬─────┘
                    └──────┬───────┘
                           ▼
                 ┌────────────────────┐
                 │ Agente Paciente    │
                 └─────────┬──────────┘
                           │
                           ▼
                  Memoria y registros
                           │
                           └──► Siguiente turno
```

El controlador alterna las intervenciones, solicita evaluaciones y actualiza el estado simulado del paciente.

## 🧠 Memoria persistente

El sistema utiliza `SQLiteSession`, una funcionalidad de OpenAI Agents SDK, para conservar los historiales de conversación.

Cada participante tiene una sesión independiente:

```python
sesion_psicologo = SQLiteSession("psicologo", DB)
sesion_paciente = SQLiteSession("marcos", DB)
```

Ambas sesiones se almacenan en el fichero `terapia_estado.db`.

Esto permite recuperar el contexto de las conversaciones anteriores después de cerrar y volver a ejecutar el programa.

La memoria implementada es conversacional. No constituye una memoria cognitiva ni garantiza una coherencia perfecta durante conversaciones prolongadas.

## 📊 Modelo de estado emocional

El paciente ficticio dispone de cinco variables sintéticas, representadas mediante valores entre 0 y 10.

| Variable | Valor inicial | Interpretación |
|---|---:|---|
| Ánimo | 3 | Estado de ánimo simulado |
| Ansiedad | 7 | Nivel de ansiedad simulado |
| Energía | 2 | Energía percibida del personaje |
| Confianza | 4 | Confianza hacia el interlocutor |
| Aislamiento | 8 | Tendencia al aislamiento social |

La evolución de estas variables se determina mediante reglas explícitas programadas en Python.

Por ejemplo, una intervención clasificada con niveles elevados de empatía y escucha puede incrementar la variable de confianza. Determinadas condiciones permiten cambios graduales en otras variables.

**Estos valores no son escalas psicológicas validadas y sus cambios no representan mejoras clínicas reales.**

## 🛠️ Tecnologías utilizadas

- **Python:** lenguaje principal.
- **OpenAI Agents SDK:** definición y ejecución de agentes.
- **Modelos OpenAI:** generación de respuestas y evaluación lingüística.
- **SQLite:** persistencia del historial conversacional.
- **Pydantic:** validación de las evaluaciones estructuradas.
- **JSON:** almacenamiento del estado simulado.
- **CSV:** registro de variables para su análisis.

## 🚀 Instalación

### Requisitos

- Python 3.10 o superior, utilizando preferiblemente una versión reciente compatible.
- Cuenta de OpenAI Platform con acceso a la API.
- Clave API válida.
- Conexión a Internet.

### 1. Clonar el repositorio

```bash
git clone https://github.com/sistemasorp/terapia_agentes_ia
cd terapia_agentes_ia
```

### 2. Crear un entorno virtual

En Windows PowerShell:

```powershell
python -m venv .venv
```

Activar el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución de scripts, puede habilitarse temporalmente para la sesión actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 3. Instalar dependencias

```powershell
python -m pip install --upgrade pip
python -m pip install openai-agents
```

### 4. Configurar la API key

En PowerShell:

```powershell
$env:OPENAI_API_KEY="TU_API_KEY"
```

La clave no debe incorporarse al código fuente ni publicarse en GitHub.

### 5. Ejecutar el experimento

```powershell
python .\terapia_estado.py
```

El programa ejecutará un número predefinido de turnos entre los agentes.

Cada turno realiza llamadas al modelo para generar la intervención del psicólogo, evaluarla y producir la respuesta del paciente.

**El uso de la API de OpenAI puede generar costes según los modelos utilizados y el volumen de tokens procesados.**

## 📁 Archivos del proyecto

```text
multi-agent-ai/
│
├── terapia_estado.py
├── README.md
├── .gitignore
│
├── terapia_estado.db       # Memoria SQLite
├── paciente_estado.json    # Estado emocional
├── control_terapia.json    # Control de turnos
└── evolucion_paciente.csv  # Evolución de variables
```

Los archivos de datos se generan durante la ejecución y no es necesario incorporarlos al repositorio.

Se recomienda utilizar el siguiente `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc
*.db
*.db-*
.env
*_estado.json
control_terapia.json
*.csv
```

## 🔬 Análisis experimental

La arquitectura permite estudiar aspectos como:

**Persistencia de contexto:** comprobar si los agentes mantienen información de conversaciones anteriores.

**Coherencia de roles:** observar si el psicólogo y el paciente ficticios mantienen comportamientos consistentes con sus instrucciones.

**Evaluación automatizada:** analizar cómo un tercer agente clasifica las características comunicativas de las intervenciones.

**Evolución del estado sintético:** representar gráficamente los cambios producidos por las reglas programadas.

**Comparación de estrategias:** ejecutar diferentes configuraciones del agente Psicólogo y comparar los resultados dentro del modelo simulado.

### Estado de los resultados

El proyecto implementa los mecanismos necesarios para generar registros experimentales, pero no se presentan aquí resultados cuantitativos verificados, comparaciones estadísticas ni conclusiones sobre eficacia clínica.

Las observaciones obtenidas dependerán de las instrucciones, el modelo seleccionado, las reglas de evolución y las condiciones de ejecución.

## ⚠️ Limitaciones

Esta prueba de concepto presenta varias limitaciones importantes:

1. **No existe validación clínica.** Los comportamientos generados no representan necesariamente los de personas reales con depresión.
2. **La empatía es una característica evaluada a partir del lenguaje.** Una respuesta aparentemente empática no demuestra comprensión emocional humana.
3. **La evolución emocional es artificial.** Las variables cambian según reglas definidas por el desarrollador.
4. **Las evaluaciones pueden contener sesgos.** El agente Evaluador puede producir puntuaciones inconsistentes.
5. **La memoria no garantiza coherencia absoluta.** Los agentes pueden generar contradicciones o interpretaciones incorrectas.
6. **Los resultados pueden variar.** Diferentes ejecuciones pueden producir conversaciones distintas.
7. **La persistencia no es completamente transaccional.** Una interrupción durante el guardado podría desincronizar algunos registros.

## 🔐 Seguridad y uso responsable

El proyecto debe utilizarse exclusivamente con personajes y datos ficticios.

No está diseñado para interactuar con pacientes reales ni para tomar decisiones relacionadas con la salud mental.

Los mecanismos de seguridad del modelo y los controles adicionales de la aplicación deben mantenerse activos.

Ante contenido que indique un posible riesgo de autolesión o suicidio, cualquier ampliación del sistema debe priorizar una respuesta de seguridad y la intervención humana apropiada, en lugar de continuar automáticamente la simulación.

## 🔮 Posibles mejoras

- Memoria a largo plazo basada en resúmenes.
- Incorporación de bases de datos vectoriales.
- Comparación de diferentes modelos de lenguaje.
- Evaluación independiente con criterios más detallados.
- Ejecuciones repetidas para estudiar variabilidad.
- Visualización de métricas mediante Grafana o herramientas similares.
- Panel web para observar las conversaciones en tiempo real.
- Registro de trazas, tokens consumidos y costes de API.
- Mejora de la reproducibilidad y de la consistencia del almacenamiento.

## 📚 Referencias

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [OpenAI API](https://platform.openai.com/docs/)
- [OpenAI Agents SDK — Sessions](https://openai.github.io/openai-agents-python/sessions/)
- [OpenAI Agents SDK — Guardrails](https://openai.github.io/openai-agents-python/guardrails/)

---

**Este repositorio documenta una exploración tecnológica sobre sistemas multiagente, memoria persistente y evaluación automatizada. No constituye investigación clínica ni pretende sustituir la intervención de profesionales de la psicología.**
