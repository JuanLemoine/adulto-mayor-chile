# 🏥 Sistema de Seguimiento Médico - Adulto Mayor Chile

Plataforma demo desarrollada en Streamlit para mejorar el seguimiento integral de pacientes y facilitar la comunicación entre médicos y pacientes.

## 📋 Características

### Funcionalidades Principales

- **✅ Registro Completo de Pacientes**
  - Nombre completo
  - Correo electrónico con validación en tiempo real
  - Número de teléfono con indicativo internacional
  - Validación de todos los campos

- **👨‍⚕️ Información del Médico**
  - Registro del médico tratante

- **💊 Prescripción Médica**
  - Campo de texto amplio para detallar medicamentos
  - Dosis, frecuencia y duración del tratamiento

- **📝 Recomendaciones**
  - Campo de texto para instrucciones de cuidado
  - Recomendaciones personalizadas para cada paciente

- **📊 Historial de Registros**
  - Almacenamiento persistente de todos los registros
  - Visualización de historial completo
  - Estadísticas en tiempo real

- **📞 Llamadas Automáticas con ElevenLabs**
  - Integración con agente conversacional de ElevenLabs
  - Llamadas automáticas al registrar un paciente
  - **Variables dinámicas**: `{{patient_name}}`, `{{doctor}}`, `{{medication}}`, `{{special_instructions}}`
  - El agente personaliza cada llamada con datos específicos del paciente y médico
  - Credenciales seguras mediante archivo `.env`
  - Confirmación de datos y entrega de información médica por voz
  - Configuración flexible (activar/desactivar)

### Diseño y Experiencia de Usuario

- 🎨 **Interfaz elegante y profesional** con gradientes modernos
- 📱 **Diseño responsivo** adaptable a diferentes dispositivos
- ✨ **Animaciones y transiciones suaves**
- 🎯 **Validaciones en tiempo real** para mejor UX
- 🔒 **Diseño formal** apropiado para entorno médico

## 🚀 Instalación y Uso

### Requisitos Previos

- Python 3.8 o superior
- Conda (recomendado) o pip

### Instalación con Conda

```bash
# Activar el entorno conda
conda activate art

# Instalar dependencias
pip install -r requirements.txt
```

### Instalación con pip

```bash
# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 📞 Configuración de ElevenLabs (Opcional)

Para habilitar las llamadas automáticas con variables dinámicas:

1. **Copia el archivo `.env.example` a `.env`**
   ```bash
   cp .env.example .env
   ```

2. **Edita el archivo `.env`** con tus credenciales de ElevenLabs:
   ```env
   ELEVENLABS_API_KEY=tu_api_key
   ELEVENLABS_AGENT_ID=tu_agent_id
   ELEVENLABS_AGENT_PHONE_NUMBER_ID=tu_phone_number_id
   ENABLE_CALLS=True
   ```

3. **Configura el System Prompt** de tu agente para usar variables dinámicas:
   - `{{patient_name}}` o `{{name}}` - Nombre del paciente
   - `{{doctor}}` - Nombre del médico tratante
   - `{{medication}}` - Prescripción médica
   - `{{special_instructions}}` - Recomendaciones

4. Consulta el archivo `VARIABLES_DINAMICAS.md` para configurar las variables
5. Consulta el archivo `CONFIGURACION_ELEVENLABS.md` para instrucciones detalladas

**Nota:** La aplicación funciona sin ElevenLabs, pero las llamadas automáticas estarán desactivadas.

## 📱 Ejecutar la Aplicación

```bash
# Activar el entorno conda
conda activate art

# Instalar dependencias (si aún no lo has hecho)
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📂 Estructura del Proyecto

```
Adulto Mayor Chile/
├── app.py                           # Aplicación principal de Streamlit
├── ejemplo_uso.py                   # Script de prueba para llamadas
├── .env                             # Credenciales de ElevenLabs (no compartir)
├── .env.example                     # Plantilla de configuración
├── requirements.txt                 # Dependencias del proyecto
├── README.md                        # Este archivo
├── GUIA_RAPIDA.md                  # Guía de inicio rápido
├── CONFIGURACION_ELEVENLABS.md     # Guía de configuración de llamadas
├── VARIABLES_DINAMICAS.md          # Guía de variables dinámicas
├── .streamlit/
│   └── config.toml                 # Configuración de Streamlit
└── registros_pacientes.json        # Base de datos de registros (se crea automáticamente)
```

## 🔧 Funcionalidades Técnicas

### Validaciones Implementadas

1. **Correo Electrónico**
   - Formato estándar (usuario@dominio.com)
   - Validación con expresiones regulares
   - Feedback visual en tiempo real

2. **Número de Teléfono**
   - Solo acepta dígitos numéricos
   - Longitud entre 7 y 15 caracteres
   - Indicativo internacional de múltiples países

3. **Campos Obligatorios**
   - Todos los campos son requeridos
   - Validación antes de guardar
   - Mensajes de error claros y específicos

### Almacenamiento de Datos

- Los registros se guardan en formato JSON
- Archivo: `registros_pacientes.json`
- Incluye timestamp de cada registro
- Datos estructurados y fáciles de exportar

## 🎨 Personalización

### Colores del Tema

Los colores principales se pueden modificar en `.streamlit/config.toml`:

```toml
primaryColor="#667eea"      # Color principal (morado)
backgroundColor="#f8f9fa"   # Fondo de la aplicación
secondaryBackgroundColor="#ffffff"  # Fondo de tarjetas
```

### Estilos CSS

Los estilos personalizados se encuentran en `app.py` en la sección de `st.markdown()` con CSS.

## 📊 Países Soportados

El sistema incluye indicativos telefónicos para:

- 🇨🇱 Chile (+56)
- 🇦🇷 Argentina (+54)
- 🇵🇪 Perú (+51)
- 🇨🇴 Colombia (+57)
- 🇲🇽 México (+52)
- 🇪🇸 España (+34)
- 🇺🇸 Estados Unidos (+1)
- 🇧🇷 Brasil (+55)
- Y más...

## 🔒 Seguridad y Privacidad

- Los datos se almacenan localmente
- No se envían datos a servidores externos
- Validación de inputs para prevenir inyecciones
- Formato JSON seguro para almacenamiento

## 🚀 Mejoras Futuras

Posibles extensiones del sistema:

- [ ] Base de datos SQL para mejor escalabilidad
- [ ] Sistema de autenticación para médicos
- [ ] Exportación a PDF de prescripciones
- [ ] Envío de correos electrónicos automáticos
- [ ] Calendario de citas
- [ ] Recordatorios de medicación
- [ ] Dashboard analítico avanzado
- [ ] Integración con sistemas de salud

## 📞 Soporte

Para preguntas o sugerencias, contactar al equipo de desarrollo.

---

**Desarrollado para Adulto Mayor Chile** | 2025

