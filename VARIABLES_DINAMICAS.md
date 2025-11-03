# 🔄 Variables Dinámicas en ElevenLabs

## ¿Qué son las Variables Dinámicas?

Las variables dinámicas permiten que tu agente de IA personalice cada llamada con información específica del paciente. El sistema ahora pasa automáticamente:

- **`name`** - Nombre del paciente (alias corto)
- **`patient_name`** - Nombre completo del paciente (recomendado)
- **`doctor`** - Nombre del médico tratante
- **`medication`** - Prescripción médica / Medicación completa
- **`special_instructions`** - Instrucciones especiales / Recomendaciones para el paciente

**Nota:** `name` y `patient_name` contienen el mismo valor. Usa el que prefieras en tu System Prompt.

## 🎯 Cómo Funciona

Cuando registras un paciente, el sistema envía estos datos a ElevenLabs:

```python
conversation_initiation_client_data={
    "dynamic_variables": {
        "name": "Juan Pérez",
        "patient_name": "Juan Pérez",
        "doctor": "Dr. María López",
        "medication": "Paracetamol 500mg cada 8 horas por 5 días",
        "special_instructions": "Reposo y líquidos abundantes"
    }
}
```

## ⚙️ Configurar el Agente en ElevenLabs

Para que tu agente use estas variables, debes configurar el **System Prompt** en ElevenLabs:

### 1️⃣ Accede a tu agente

Ve a: https://elevenlabs.io/app/conversational-ai y selecciona tu agente.

### 2️⃣ Configura el System Prompt

En la sección "Prompt" o "System Instructions", usa este ejemplo:

```
Eres un asistente médico profesional y empático del Sistema de Seguimiento Médico de Adulto Mayor Chile.

INFORMACIÓN DEL PACIENTE:
- Nombre del paciente: {{patient_name}}
- Médico tratante: {{doctor}}
- Medicación prescrita: {{medication}}
- Instrucciones especiales: {{special_instructions}}

INSTRUCCIONES:

1. SALUDO INICIAL:
   - Saluda cordialmente y preséntate
   - Menciona que llamas del Sistema de Seguimiento Médico
   - Ejemplo: "Hola {{patient_name}}, buenos días. Te hablo del Sistema de Seguimiento Médico de Adulto Mayor Chile."

2. VERIFICACIÓN:
   - Confirma que estás hablando con la persona correcta
   - Ejemplo: "¿Eres {{patient_name}}?"

3. PROPÓSITO DE LA LLAMADA:
   - Explica que acabas de recibir información de {{doctor}}
   - Menciona que vas a compartir detalles importantes sobre su tratamiento

4. MEDICACIÓN PRESCRITA:
   - Lee claramente la medicación: {{medication}}
   - Asegúrate de que el paciente entienda cada medicamento
   - Responde cualquier pregunta sobre dosis o frecuencia

5. INSTRUCCIONES ESPECIALES:
   - Comparte las instrucciones especiales: {{special_instructions}}
   - Enfatiza la importancia de seguir estas indicaciones

6. PREGUNTAS:
   - Pregunta si tiene alguna duda
   - Aclara cualquier inquietud de manera profesional

7. DESPEDIDA:
   - Recuerda que puede llamar al médico si tiene emergencias
   - Desea pronta recuperación
   - Despídete cordialmente

TONO:
- Profesional y empático
- Claro y pausado
- Paciente y amable
- Tranquilizador

IMPORTANTE:
- Siempre usa el nombre del paciente ({{patient_name}}) para personalizar
- Lee la medicación completa tal como está en {{medication}}
- Menciona todas las instrucciones en {{special_instructions}}
- No inventes información médica
- Si no sabes algo, recomienda contactar al médico tratante

VARIABLES DISPONIBLES:
- Puedes usar {{name}} o {{patient_name}} (ambos tienen el mismo valor)
- {{doctor}} para mencionar al médico
- {{medication}} para la prescripción
- {{special_instructions}} para las recomendaciones
```

## 📋 Ejemplo de Conversación

**Agente:** "Hola Juan Pérez, buenos días. Te hablo del Sistema de Seguimiento Médico de Adulto Mayor Chile. ¿Eres Juan Pérez?"

**Paciente:** "Sí, soy yo."

**Agente:** "Perfecto. Te llamo porque acabamos de recibir información de la Dra. María López y quiero compartir contigo los detalles de tu tratamiento. Tu medicación prescrita es la siguiente: Paracetamol 500mg, debes tomar 1 tableta cada 8 horas por 5 días. ¿Te queda claro?"

**Paciente:** "Sí, entendido."

**Agente:** "Excelente. Además, tienes las siguientes instrucciones especiales: Reposo en cama, tomar abundante líquido de 2 a 3 litros por día, y acudir a control en 7 días. ¿Tienes alguna pregunta sobre el tratamiento?"

**Paciente:** "No, todo claro."

**Agente:** "Perfecto Juan. Recuerda que si presentas alguna complicación o tienes dudas, puedes contactar a la Dra. María López. Te deseo una pronta recuperación. ¡Que te mejores pronto!"

## 🧪 Probar las Variables

### Opción 1: Usar la aplicación Streamlit

1. Ejecuta: `streamlit run app.py`
2. Registra un paciente con todos los datos
3. El sistema automáticamente enviará las variables

### Opción 2: Script de prueba

Puedes modificar `ejemplo_uso.py` para probar con variables personalizadas:

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="tu_api_key",
    base_url="https://api.elevenlabs.io"
)

response = client.conversational_ai.twilio.outbound_call(
    agent_id="tu_agent_id",
    agent_phone_number_id="tu_phone_number_id",
    to_number="+56912345678",
    conversation_initiation_client_data={
        "dynamic_variables": {
            "name": "María González",
            "doctor": "Dr. Carlos Ruiz",
            "medication": "Ibuprofeno 400mg cada 12 horas",
            "special_instructions": "Reposo y control en 5 días"
        }
    }
)
```

## 🎨 Personalización Adicional

Puedes agregar más variables dinámicas editando el archivo `app.py`:

En la función `hacer_llamada_elevenlabs`, puedes agregar más datos:

```python
dynamic_variables = {
    "name": nombre_paciente,
    "doctor": nombre_medico,
    "medication": medication,
    "special_instructions": special_instructions,
    "fecha": fecha_registro,   # Nuevo
    "telefono": telefono       # Nuevo
}
```

Y luego usarlos en tu System Prompt:

```
Fecha de registro: {{fecha}}
Teléfono de contacto: {{telefono}}
```

## 🔐 Uso de Variables de Entorno (.env)

Las credenciales de ElevenLabs ahora se leen desde un archivo `.env` para mayor seguridad:

### Estructura del archivo `.env`:
```env
ELEVENLABS_API_KEY=sk_xxxxxxxxxxxxx
ELEVENLABS_AGENT_ID=agent_xxxxxxxxxx
ELEVENLABS_AGENT_PHONE_NUMBER_ID=phnum_xxxxxxxxx
ENABLE_CALLS=True
```

### Ventajas:
- ✅ **Seguridad**: Las credenciales no están en el código
- ✅ **Portabilidad**: Fácil cambiar credenciales sin tocar el código
- ✅ **Git-friendly**: `.env` está en `.gitignore` por defecto
- ✅ **Equipo**: Cada desarrollador puede tener sus propias credenciales

## ✅ Verificar que Funciona

Después de configurar el System Prompt:

1. Haz una llamada de prueba
2. El agente debe usar el nombre del paciente
3. Debe leer la prescripción completa
4. Debe mencionar las recomendaciones

Si el agente no usa las variables:

- Verifica que hayas guardado el System Prompt
- Asegúrate de usar la sintaxis correcta: `{{nombre_variable}}`
- Revisa los logs en el dashboard de ElevenLabs

## 📞 Beneficios

✅ **Personalización**: Cada paciente recibe una llamada única con su nombre  
✅ **Precisión**: El agente lee exactamente la prescripción del médico  
✅ **Eficiencia**: No necesitas configurar manualmente cada llamada  
✅ **Escalabilidad**: Funciona para cualquier número de pacientes  

## 🔍 Debugging

Si las variables no funcionan:

1. **Verifica en el código** (línea 222-237 de `app.py`):
```python
dynamic_variables = {
    "name": nombre_paciente,
    "patient_name": nombre_paciente,
    "doctor": nombre_medico,
    "medication": medication,
    "special_instructions": special_instructions
}
```

2. **Verifica el archivo `.env`**:
- Asegúrate de que exista en el directorio raíz
- Verifica que las credenciales sean correctas

3. **Verifica el System Prompt** en ElevenLabs:
- Usa `{{patient_name}}` o `{{name}}`, `{{doctor}}`, `{{medication}}`, `{{special_instructions}}`
- Las llaves dobles son importantes: `{{ }}`
- No uses `{name}` ni `$name`
- Recomendado: Usa `{{patient_name}}` para mayor claridad

3. **Revisa los logs** en ElevenLabs Dashboard:
- Ve a Conversations
- Busca tu llamada
- Verifica que las variables se hayan enviado

## 💡 Tips

- **Nombres claros**: Usa nombres descriptivos para las variables
- **Formato consistente**: Mantén el formato de las variables igual en código y prompt
- **Testing**: Prueba con diferentes valores antes de usar en producción
- **Documentación**: Mantén un registro de qué variables usas

---

**¿Necesitas más variables?** Edita `app.py` en las líneas 181-227 para agregar más campos dinámicos.

