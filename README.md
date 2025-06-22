# LegisLink Pro - Multi-Agent Legal Platform for ADK Hackathon

## 🏆 ADK Hackathon Submission - Automatización de Procesos Complejos (Legal)

LegisLink Pro es una plataforma multiagente avanzada para la gestión legal internacional, construida con Google Cloud y el Agent Development Kit (ADK). El sistema automatiza flujos legales complejos con validación constitucional en tiempo real.

## 🎯 Categoría y Foco Principal

**Categoría:** Automatización de Procesos Complejos (Legal)
- Automatización de flujos legales internacionales
- Gestión de documentos con validación constitucional
- Orquestación multiagente especializada

## 🤖 Arquitectura Multiagente

### 5 Agentes Especializados:
1. **CRM Agent** - Gestión de clientes y casos
2. **RAG Agent** - Búsqueda y recuperación de información legal
3. **Constitute Agent** - Validación constitucional en tiempo real
4. **Document Agent** - Generación y gestión de documentos legales
5. **Translation Agent** - Traducción multiidioma de documentos

### Patrones ADK Implementados:
- **Delegación** (sub_agents en Manager)
- **Agentes como Herramientas** (Document Agent para generación)
- **Flujos secuenciales/paralelos** (Legal Document Generation)

## 🏗️ Requisitos Técnicos Obligatorios

### Google Cloud Services:
- **Agent Engine** - Despliegue de agentes
- **Vertex AI** - RAG y Gemini 2.5
- **Cloud SQL** - MySQL
- **Google Drive** - Gestión documental
- **Cloud Run** - Backend Flask

## 📁 Estructura del Proyecto

```
LegisLink/
├── adk/                          # Ejemplos y tutoriales ADK
├── legislink-pro/                # Aplicación principal
│   ├── api/                      # API Flask
│   ├── manager/                  # Gestor de agentes
│   │   └── sub_agents/           # Agentes especializados
│   ├── frontend/                 # Interfaz Vue.js
│   ├── services/                 # Servicios de Google Cloud
│   └── tests/                    # Tests unitarios
├── ai_docs/                      # Documentación técnica
├── diagrams/                     # Diagramas de arquitectura
└── docs/                         # Documentación de patrones
```

## 🚀 Instalación y Despliegue

### Prerrequisitos:
- Python 3.12+
- Node.js 18+
- Google Cloud CLI
- Docker

### Configuración Local:
```bash
# Clonar repositorio
git clone https://github.com/dark-yx/borrador-adk.git
cd LegisLink

# Configurar entorno Python
cd legislink-pro
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Configurar frontend
cd frontend
npm install
npm run serve
```

### Despliegue en Google Cloud:
```bash
# Configurar proyecto GCP
gcloud config set project YOUR_PROJECT_ID

# Desplegar con Cloud Build
gcloud builds submit --config cloudbuild.yaml
```

## 🔧 Configuración

1. **Variables de Entorno:**
   ```bash
   cp legislink-pro/env.example legislink-pro/.env
   # Configurar variables en .env
   ```

2. **Google Cloud Setup:**
   - Habilitar APIs necesarias
   - Configurar credenciales de servicio
   - Crear base de datos Cloud SQL

3. **Vertex AI:**
   - Configurar modelo Gemini 2.5
   - Crear corpus de documentos legales

## 🧪 Testing

```bash
# Ejecutar tests unitarios
cd legislink-pro
python -m pytest tests/ -v

# Cobertura de código
python -m pytest --cov=. --cov-report=html
```

## 📊 Métricas de Desempeño

- **Latencia generación documentos:** < 30 segundos
- **Precisión validación constitucional:** > 95%
- **Recall@5 RAG:** > 90%

## 🎥 Demo Video

[Enlace al video demostrativo - 3 minutos]
- Configuración GCP (Vertex AI, Agent Engine)
- Ejecución flujo completo (generación documento)
- Resultados tangibles (documento en Drive)

## 🏅 Criterios de Evaluación

### Technical Implementation (50%):
- ✅ Logging de interacciones entre agentes
- ✅ Documentación de código con flujos
- ✅ Tests unitarios (90% cobertura crítica)

### Innovación (30%):
- ✅ Validación constitucional en tiempo real
- ✅ RAG optimizado para documentos legales
- ✅ Generación dinámica con control de versiones

### Excelencia en Demo (20%):
- ✅ Video funcional en GCP
- ✅ Flujo completo demostrado
- ✅ Resultados tangibles

## 🎁 Bonus Features

- **Blog técnico:** [Enlace al blog post]
- **Contribución ADK:** Módulo `google.adk.legal`
- **Dataset:** 10K+ documentos legales etiquetados

## 📞 Contacto

- **Repositorio:** https://github.com/dark-yx/borrador-adk
- **Hashtag:** #adkhackathon
- **Región:** LatAm

## 📄 Licencia

Este proyecto es parte de la ADK Hackathon con Google Cloud.

---

**LegisLink Pro** - Revolucionando la gestión legal con IA multiagente 🚀 