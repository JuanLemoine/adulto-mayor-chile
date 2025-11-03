# 🚀 Guía Rápida - Sistema de Seguimiento Médico con ElevenLabs

## ¿Qué hace esta aplicación?

Una plataforma elegante en Streamlit que permite a los médicos:
1. **Registrar pacientes** con validación de datos
2. **Escribir prescripciones** médicas y recomendaciones
3. **Llamar automáticamente** al paciente vía ElevenLabs

## 🎯 Flujo de Trabajo

```
┌─────────────────────────────────────────────────────────────────┐
│  1. MÉDICO REGISTRA PACIENTE                                    │
│                                                                  │
│  ✓ Nombre: Juan Pérez                                          │
│  ✓ Correo: juan@email.com (validación automática)             │
│  ✓ Teléfono: +56912345678 (con indicativo)                    │
│  ✓ Prescripción: Paracetamol 500mg cada 8h por 5 días         │
│  ✓ Recomendaciones: Reposo, líquidos, control en 7 días       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. SISTEMA GUARDA INFORMACIÓN                                  │
│                                                                  │
│  📁 Registro guardado en registros_pacientes.json              │
│  ⏰ Timestamp: 2025-11-02 14:30:00                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. ELEVENLABS HACE LA LLAMADA                                  │
│                                                                  │
│  📞 API de ElevenLabs → Twilio → Llamada al paciente          │
│  🤖 Agente de IA conversa con el paciente                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. PACIENTE RECIBE LA LLAMADA                                  │
│                                                                  │
│  🗣️  "Hola, llamo del Sistema de Seguimiento Médico..."       │
│  📋 Confirma datos                                              │
│  💊 Informa sobre prescripción                                  │
│  📝 Entrega recomendaciones                                     │
│  ❓ Responde preguntas                                          │
└─────────────────────────────────────────────────────────────────┘
```

## 🔧 Configuración Inicial (3 pasos)

### Paso 1: Editar las credenciales en `app.py`

```python
# Abre: app.py (líneas 14-17)

ELEVENLABS_API_KEY = "sk_xxxxx..."  # Tu API key de ElevenLabs
ELEVENLABS_AGENT_ID = "agent_xxxxx..."  # Tu Agent ID
ELEVENLABS_AGENT_PHONE_NUMBER_ID = "phnum_xxxxx..."  # Tu Phone Number ID
ENABLE_CALLS = True  # Activar llamadas
```

Las credenciales están al inicio del archivo `app.py`, justo después de los imports.

### Paso 2: Ejecutar la aplicación

```bash
conda activate art
streamlit run app.py
```

### Paso 3: ¡Listo! 🎉

Navega a `http://localhost:8501` y comienza a registrar pacientes.

## 📞 ¿Cómo obtener las credenciales de ElevenLabs?

### 1️⃣ API Key
- Ve a: https://elevenlabs.io/app/settings/api-keys
- Click en "Create new key"
- Copia la key

### 2️⃣ Agent ID
- Ve a: https://elevenlabs.io/app/conversational-ai
- Crea o selecciona un agente
- Copia el ID del agente

### 3️⃣ Agent Phone Number ID
- En tu agente, ve a "Phone Numbers"
- Configura Twilio integration
- Copia el Phone Number ID

**Consulta `CONFIGURACION_ELEVENLABS.md` para instrucciones detalladas.**

## 🎨 Características de la Interfaz

### ✅ Validación en Tiempo Real
- **Correo:** Muestra ✅ o ❌ según el formato
- **Teléfono:** Valida que sean solo números

### 🌍 Indicativos Internacionales
Soporta múltiples países:
- 🇨🇱 Chile (+56)
- 🇦🇷 Argentina (+54)
- 🇨🇴 Colombia (+57)
- Y más...

### 📊 Historial de Registros
- Ver todos los registros anteriores
- Estadísticas en el sidebar
- Exportación de datos en JSON

### 🎭 Diseño Elegante
- Gradiente morado profesional
- Animaciones suaves
- Interfaz intuitiva

## 🔒 Seguridad

⚠️ **IMPORTANTE:**
- NO compartas tu API key públicamente
- Ten cuidado al compartir el archivo `app.py` ya que contiene tus credenciales
- Si usas Git, considera usar un archivo `.env` separado para las credenciales

## 🐛 Problemas Comunes

### "API Key no configurada"
➡️ Edita las líneas 14-17 de `app.py` con tus credenciales reales

### "Error al hacer la llamada"
➡️ Verifica:
- API Key correcta
- Agent ID correcto
- Phone Number ID correcto
- Saldo en tu cuenta de ElevenLabs
- Número de teléfono con formato correcto (+573102095609)

### La app no inicia
➡️ Verifica:
```bash
conda activate art
pip install -r requirements.txt
```

## 💡 Tips Útiles

### Desactivar llamadas temporalmente
```python
# En app.py (línea 17)
ENABLE_CALLS = False
```

### Personalizar el agente de IA
Ve a ElevenLabs → tu agente → System Prompt:
```
Eres un asistente médico profesional y empático.
Saluda cordialmente y confirma datos del paciente.
Proporciona información sobre prescripciones de manera clara.
Mantén un tono profesional y tranquilizador.
```

### Ver los registros guardados
```bash
cat registros_pacientes.json
```

## 📱 Ejemplo de Uso Real

```
1. Médico abre la app
2. Completa el formulario:
   - Nombre: María González
   - Correo: maria@email.com
   - Teléfono: +56987654321 (Chile)
   - Prescripción: "Ibuprofeno 400mg cada 12 horas..."
   - Recomendaciones: "Reposo, control en 5 días..."
   
3. Click en "Registrar Información del Paciente"

4. Sistema:
   ✅ Guarda el registro
   📞 Inicia llamada automática
   🎉 Muestra confirmación

5. Paciente recibe la llamada del agente de IA

6. Médico puede ver el registro en "Ver Todos los Registros"
```

## 🎯 Próximos Pasos

Una vez que tengas todo funcionando:

1. ✅ Prueba con un número de prueba
2. ✅ Personaliza el agente de IA
3. ✅ Ajusta el System Prompt
4. ✅ Prueba con pacientes reales

## 📚 Más Información

- `README.md` - Documentación completa
- `CONFIGURACION_ELEVENLABS.md` - Guía detallada de ElevenLabs
- [ElevenLabs Docs](https://elevenlabs.io/docs)

---

**¿Listo para empezar?** 🚀

```bash
conda activate art
streamlit run app.py
```

¡Y comienza a mejorar el seguimiento de tus pacientes! 🏥

