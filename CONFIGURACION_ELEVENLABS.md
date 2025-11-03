# 📞 Configuración de ElevenLabs para Llamadas Automáticas

Este documento explica cómo configurar las llamadas automáticas con ElevenLabs cuando se registra un paciente.

## 🔧 Pasos de Configuración

### 1. Obtener API Key de ElevenLabs

1. Ve a https://elevenlabs.io/ y crea una cuenta o inicia sesión
2. Navega a **Settings** → **API Keys**
3. Copia tu API Key

### 2. Configurar tu Agente Conversacional

1. Ve a https://elevenlabs.io/app/conversational-ai
2. Crea un nuevo agente o selecciona uno existente
3. Copia el **Agent ID** (tiene formato: `agent_xxxxxxxxxxxxxx`)

### 3. Configurar Integración con Twilio

ElevenLabs necesita un número de teléfono de Twilio para hacer llamadas salientes:

1. En tu agente de ElevenLabs, ve a **Phone Numbers**
2. Importa tu número de Twilio usando SIP Trunk
3. Copia el **Agent Phone Number ID** (tiene formato: `phnum_xxxxxxxxxxxxxx`)

**Nota:** Necesitas una cuenta de Twilio y un número de teléfono configurado. Consulta la documentación de ElevenLabs para más detalles:
https://elevenlabs.io/docs/conversational-ai/integrations/twilio

### 4. Configurar las Credenciales en la Aplicación

Abre el archivo `app.py` y edita las líneas 14-17 al inicio del archivo:

```python
# ============================
# CONFIGURACIÓN DE ELEVENLABS
# ============================

ELEVENLABS_API_KEY = "sk_xxxxxxxxxxxxxxxxxxxxx"  # Tu API key
ELEVENLABS_AGENT_ID = "agent_xxxxxxxxxxxxxx"  # Tu agent_id
ELEVENLABS_AGENT_PHONE_NUMBER_ID = "phnum_xxxxxxxxxxxxxx"  # Tu agent_phone_number_id
ENABLE_CALLS = True  # True para activar, False para desactivar
```

### 5. Instalar Dependencias

Si aún no has instalado las dependencias, ejecuta:

```bash
conda activate art
pip install -r requirements.txt
```

## 🚀 Cómo Funciona

1. Cuando se registra un paciente en la plataforma, el sistema guarda todos los datos
2. Automáticamente, se inicia una llamada al número de teléfono registrado
3. El agente conversacional de ElevenLabs contactará al paciente
4. El agente puede:
   - Confirmar los datos del registro
   - Leer la prescripción médica
   - Proporcionar las recomendaciones
   - Responder preguntas del paciente

## 🎯 Personalizar el Agente

Para que el agente proporcione información relevante al paciente:

1. Ve a tu agente en ElevenLabs
2. Configura el **System Prompt** con instrucciones como:

```
Eres un asistente médico virtual profesional y empático. Cuando llames a un paciente:

1. Saluda cordialmente y presenta tu propósito
2. Confirma que estás llamando de parte del sistema de seguimiento médico
3. Verifica la identidad del paciente
4. Informa sobre su cita o registro médico
5. Si el paciente lo solicita, proporciona información sobre su prescripción médica
6. Responde preguntas de manera clara y profesional
7. Finaliza la llamada cordialmente

Mantén siempre un tono profesional, empático y tranquilizador.
```

3. Ajusta la voz, velocidad y otros parámetros según tu preferencia

## 🔒 Seguridad

- **NUNCA** compartas tu API key en repositorios públicos
- Si usas Git, considera mover las credenciales a un archivo `.env` y usar variables de entorno
- Las credenciales están al inicio de `app.py` - ten cuidado al compartir el código
- Asegúrate de cumplir con las regulaciones de privacidad de datos médicos

## ⚙️ Desactivar Llamadas Temporalmente

Si necesitas desactivar las llamadas sin eliminar la configuración:

En `app.py` (línea 17), cambia:
```python
ENABLE_CALLS = False
```

## 🐛 Solución de Problemas

### Error: "API Key de ElevenLabs no configurada"
- Verifica que hayas editado las credenciales en las líneas 14-17 de `app.py`

### Error al hacer la llamada
- Verifica que tu Agent ID y Agent Phone Number ID sean correctos
- Asegúrate de que tu número de Twilio esté correctamente configurado
- Verifica que tengas saldo en tu cuenta de ElevenLabs
- Revisa los logs en el panel de ElevenLabs

### El agente no dice lo esperado
- Ajusta el System Prompt en la configuración del agente
- Configura el Knowledge Base si necesitas que tenga información específica

## 📚 Recursos Adicionales

- [Documentación de ElevenLabs Conversational AI](https://elevenlabs.io/docs/conversational-ai)
- [Integración con Twilio](https://elevenlabs.io/docs/conversational-ai/integrations/twilio)
- [API Reference](https://elevenlabs.io/docs/api-reference)

## 💡 Ejemplo de Uso

Cuando un médico registra a un paciente:

1. **Registro en Streamlit:**
   - Nombre: Juan Pérez
   - Teléfono: +56912345678
   - Prescripción: Paracetamol 500mg cada 8 horas

2. **El sistema automáticamente:**
   - Guarda el registro
   - Inicia llamada a +56912345678
   - ElevenLabs contacta al paciente

3. **El agente de IA:**
   - "Hola, buenos días. Llamo del Sistema de Seguimiento Médico..."
   - Confirma datos
   - Informa sobre la prescripción
   - Responde preguntas

---

**¿Necesitas ayuda?** Consulta la documentación oficial de ElevenLabs o contacta al equipo de soporte.

