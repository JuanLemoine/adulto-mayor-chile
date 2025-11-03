import streamlit as st
import re
import pandas as pd
from datetime import datetime
import json
import os
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

# ============================
# CONFIGURACIÓN DE ELEVENLABS
# ============================
# Cargar variables de entorno desde el archivo .env
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID")
ELEVENLABS_AGENT_PHONE_NUMBER_ID = os.getenv("ELEVENLABS_AGENT_PHONE_NUMBER_ID")
ENABLE_CALLS = os.getenv("ENABLE_CALLS", "True").lower() == "true"

# ============================

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Seguimiento Médico",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para un diseño elegante y formal
st.markdown("""
    <style>
    /* Estilos generales */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Encabezado principal */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .header-subtitle {
        color: #e0e7ff;
        font-size: 1.1rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Tarjetas de sección */
    .section-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        color: #667eea;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    /* Botones */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        box-shadow: 0 6px 8px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }
    
    /* Inputs */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border: 2px solid #e5e7eb;
        border-radius: 6px;
        padding: 0.5rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Mensajes de éxito y error */
    .success-message {
        background-color: #d1fae5;
        color: #065f46;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
    
    .error-message {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid #e5e7eb;
    }
    
    /* Labels */
    label {
        color: #374151;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f3f4f6;
    }
    </style>
""", unsafe_allow_html=True)

# Códigos de país para teléfonos
COUNTRY_CODES = {
    "🇨🇱 Chile (+56)": "+56",
    "🇦🇷 Argentina (+54)": "+54",
    "🇵🇪 Perú (+51)": "+51",
    "🇨🇴 Colombia (+57)": "+57",
    "🇲🇽 México (+52)": "+52",
    "🇪🇸 España (+34)": "+34",
    "🇺🇸 Estados Unidos (+1)": "+1",
    "🇧🇷 Brasil (+55)": "+55",
    "🇺🇾 Uruguay (+598)": "+598",
    "🇵🇾 Paraguay (+595)": "+595",
    "🇧🇴 Bolivia (+591)": "+591",
    "🇪🇨 Ecuador (+593)": "+593",
    "🇻🇪 Venezuela (+58)": "+58",
}

def validar_email(email):
    """Valida el formato del correo electrónico"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def validar_telefono(telefono):
    """Valida que el teléfono contenga solo números"""
    return telefono.isdigit() and len(telefono) >= 7 and len(telefono) <= 15

def hacer_llamada_elevenlabs(numero_telefono, nombre_paciente="", nombre_medico="", medication="", special_instructions=""):
    """
    Realiza una llamada saliente (outbound) usando ElevenLabs con variables dinámicas
    
    Args:
        numero_telefono: Número completo con indicativo (ej: +573102095609)
        nombre_paciente: Nombre del paciente para personalizar la llamada
        nombre_medico: Nombre del médico tratante (opcional)
        medication: Prescripción médica / Medicación (opcional)
        special_instructions: Recomendaciones / Instrucciones especiales (opcional)
    
    Returns:
        dict: Resultado de la llamada con status y mensaje
    """
    try:
        # Verificar si las llamadas están habilitadas
        if not ENABLE_CALLS:
            return {
                "success": False,
                "message": "Las llamadas automáticas están desactivadas en la configuración"
            }
        
        # Verificar credenciales básicas
        if not ELEVENLABS_API_KEY or not ELEVENLABS_AGENT_ID or not ELEVENLABS_AGENT_PHONE_NUMBER_ID:
            return {
                "success": False,
                "message": "⚠️ Credenciales de ElevenLabs incompletas. Verifica las líneas 14-17 en app.py"
            }
        
        # Limpiar el número de teléfono (remover espacios)
        numero_limpio = numero_telefono.replace(" ", "")
        
        # Inicializar cliente de ElevenLabs
        client = ElevenLabs(
            api_key=ELEVENLABS_API_KEY,
            base_url="https://api.elevenlabs.io"
        )
        
        # Preparar variables dinámicas para personalizar la llamada
        dynamic_variables = {
            "name": nombre_paciente,
            "patient_name": nombre_paciente  # Alias para mayor compatibilidad
        }
        
        # Agregar doctor si está disponible
        if nombre_medico:
            dynamic_variables["doctor"] = nombre_medico
        
        # Agregar medication si está disponible
        if medication:
            dynamic_variables["medication"] = medication
        
        # Agregar special_instructions si están disponibles
        if special_instructions:
            dynamic_variables["special_instructions"] = special_instructions
        
        # Realizar llamada saliente usando Twilio (según documentación oficial)
        # https://elevenlabs.io/docs/agents-platform/api-reference/twilio/outbound-call
        response = client.conversational_ai.twilio.outbound_call(
            agent_id=ELEVENLABS_AGENT_ID,
            agent_phone_number_id=ELEVENLABS_AGENT_PHONE_NUMBER_ID,
            to_number=numero_limpio,
            conversation_initiation_client_data={
                "dynamic_variables": dynamic_variables
            }
        )
        
        return {
            "success": True,
            "message": f"✅ Llamada iniciada exitosamente al número {numero_telefono}",
            "response": response
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error al realizar la llamada: {str(e)}"
        }

def guardar_registro(datos):
    """Guarda el registro en un archivo JSON"""
    archivo = 'registros_pacientes.json'
    
    # Crear archivo si no existe
    if not os.path.exists(archivo):
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    # Leer registros existentes
    with open(archivo, 'r', encoding='utf-8') as f:
        registros = json.load(f)
    
    # Agregar nuevo registro
    registros.append(datos)
    
    # Guardar todos los registros
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(registros, f, indent=4, ensure_ascii=False)

def main():
    # Encabezado principal
    st.markdown("""
        <div class="header-container">
            <h1 class="header-title">🏥 Sistema de Seguimiento Médico</h1>
            <p class="header-subtitle">Plataforma de Gestión Integral para Pacientes y Profesionales de la Salud</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar con información
    with st.sidebar:
        st.markdown("### 📋 Información del Sistema")
        st.markdown("""
        Este sistema permite:
        - ✅ Registro completo de pacientes
        - ✅ Validación de datos
        - ✅ Prescripciones médicas
        - ✅ Recomendaciones personalizadas
        - ✅ Historial de registros
        - 📞 Llamadas automáticas con ElevenLabs
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Estadísticas")
        
        # Mostrar estadísticas si existen registros
        if os.path.exists('registros_pacientes.json'):
            with open('registros_pacientes.json', 'r', encoding='utf-8') as f:
                registros = json.load(f)
                st.metric("Total de Pacientes", len(registros))
        else:
            st.metric("Total de Pacientes", 0)
        
        st.markdown("---")
        st.markdown("### 🔍 Ver Registros")
        if st.button("📄 Ver Todos los Registros"):
            st.session_state.mostrar_registros = True
    
    # Mostrar registros si se solicita
    if 'mostrar_registros' in st.session_state and st.session_state.mostrar_registros:
        st.markdown("---")
        st.markdown("## 📋 Historial de Registros")
        
        if os.path.exists('registros_pacientes.json'):
            with open('registros_pacientes.json', 'r', encoding='utf-8') as f:
                registros = json.load(f)
                
            if registros:
                for idx, registro in enumerate(reversed(registros), 1):
                    with st.expander(f"Paciente: {registro['nombre']} - {registro['fecha_registro']}", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Correo:** {registro['correo']}")
                            st.markdown(f"**Teléfono:** {registro['telefono_completo']}")
                        with col2:
                            st.markdown(f"**Médico:** Dr. {registro['nombre_medico']}")
                            st.markdown(f"**Fecha:** {registro['fecha_registro']}")
                        
                        st.markdown("**Prescripción Médica:**")
                        st.info(registro['prescripcion'])
                        
                        st.markdown("**Recomendaciones:**")
                        st.success(registro['recomendaciones'])
            else:
                st.info("No hay registros disponibles.")
        else:
            st.info("No hay registros disponibles.")
        
        if st.button("🔙 Cerrar Registros"):
            st.session_state.mostrar_registros = False
            st.rerun()
        
        st.markdown("---")
    
    # Formulario principal
    st.markdown("## 👤 Información del Paciente")
    
    with st.container():
        # Información del paciente
        col1, col2 = st.columns(2)
        
        with col1:
            nombre_paciente = st.text_input(
                "Nombre Completo del Paciente *",
                placeholder="Ej: Juan Pérez González",
                help="Ingrese el nombre completo del paciente"
            )
        
        with col2:
            correo_paciente = st.text_input(
                "Correo Electrónico *",
                placeholder="ejemplo@correo.com",
                help="Ingrese un correo electrónico válido"
            )
        
        # Validación de correo en tiempo real
        if correo_paciente:
            if validar_email(correo_paciente):
                st.markdown('<p style="color: #10b981; font-size: 0.9rem;">✅ Correo válido</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color: #ef4444; font-size: 0.9rem;">❌ Formato de correo inválido</p>', unsafe_allow_html=True)
    
    # Teléfono con indicativo
    st.markdown("### 📱 Número de Teléfono")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        indicativo = st.selectbox(
            "Indicativo País *",
            options=list(COUNTRY_CODES.keys()),
            help="Seleccione el código de país"
        )
    
    with col2:
        telefono = st.text_input(
            "Número de Teléfono *",
            placeholder="912345678",
            help="Ingrese solo números, sin espacios ni guiones",
            max_chars=15
        )
    
    # Validación de teléfono
    if telefono:
        if validar_telefono(telefono):
            telefono_completo = f"{COUNTRY_CODES[indicativo]} {telefono}"
            st.markdown(f'<p style="color: #10b981; font-size: 0.9rem;">✅ Teléfono: {telefono_completo}</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #ef4444; font-size: 0.9rem;">❌ Ingrese solo números (7-15 dígitos)</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Información del médico
    st.markdown("## 👨‍⚕️ Información del Médico")
    nombre_medico = st.text_input(
        "Nombre del Médico Tratante *",
        placeholder="Ej: Dr. María López",
        help="Ingrese el nombre del médico responsable"
    )
    
    st.markdown("---")
    
    # Prescripción médica
    st.markdown("## 💊 Prescripción Médica")
    prescripcion = st.text_area(
        "Detalle de la Prescripción *",
        placeholder="""Ejemplo:
        
- Paracetamol 500mg - 1 tableta cada 8 horas por 5 días
- Ibuprofeno 400mg - 1 tableta cada 12 horas por 3 días
- Descanso relativo por 7 días
        
Indique medicamentos, dosis, frecuencia y duración del tratamiento.""",
        height=200,
        help="Escriba la prescripción médica completa con todos los detalles necesarios"
    )
    
    st.markdown("---")
    
    # Recomendaciones
    st.markdown("## 📝 Recomendaciones para el Paciente")
    recomendaciones = st.text_area(
        "Recomendaciones y Cuidados *",
        placeholder="""Ejemplo:
        
- Tomar abundante líquido (2-3 litros de agua al día)
- Mantener reposo en cama
- Evitar esfuerzos físicos intensos
- Consumir alimentos ligeros y nutritivos
- Acudir a control médico en 7 días
- En caso de fiebre mayor a 38.5°C, acudir a urgencias
        
Indique todas las recomendaciones importantes para la recuperación del paciente.""",
        height=200,
        help="Escriba las recomendaciones y cuidados que debe seguir el paciente"
    )
    
    st.markdown("---")
    
    # Botón de envío
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("📋 Registrar Información del Paciente", use_container_width=True):
            # Validaciones
            errores = []
            
            if not nombre_paciente:
                errores.append("El nombre del paciente es obligatorio")
            
            if not correo_paciente:
                errores.append("El correo electrónico es obligatorio")
            elif not validar_email(correo_paciente):
                errores.append("El formato del correo electrónico es inválido")
            
            if not telefono:
                errores.append("El número de teléfono es obligatorio")
            elif not validar_telefono(telefono):
                errores.append("El número de teléfono debe contener solo dígitos (7-15)")
            
            if not nombre_medico:
                errores.append("El nombre del médico es obligatorio")
            
            if not prescripcion or len(prescripcion.strip()) < 10:
                errores.append("La prescripción médica debe contener al menos 10 caracteres")
            
            if not recomendaciones or len(recomendaciones.strip()) < 10:
                errores.append("Las recomendaciones deben contener al menos 10 caracteres")
            
            # Mostrar errores o guardar
            if errores:
                st.markdown('<div class="error-message">', unsafe_allow_html=True)
                st.markdown("### ❌ Errores en el formulario:")
                for error in errores:
                    st.markdown(f"- {error}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                # Guardar registro
                datos_registro = {
                    "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "nombre": nombre_paciente,
                    "correo": correo_paciente,
                    "indicativo": COUNTRY_CODES[indicativo],
                    "telefono": telefono,
                    "telefono_completo": f"{COUNTRY_CODES[indicativo]} {telefono}",
                    "nombre_medico": nombre_medico,
                    "prescripcion": prescripcion,
                    "recomendaciones": recomendaciones
                }
                
                guardar_registro(datos_registro)
                
                # Realizar llamada automática con ElevenLabs
                telefono_para_llamar = f"{COUNTRY_CODES[indicativo]}{telefono}"
                
                with st.spinner('📞 Iniciando llamada al paciente...'):
                    resultado_llamada = hacer_llamada_elevenlabs(
                        numero_telefono=telefono_para_llamar,
                        nombre_paciente=nombre_paciente,
                        nombre_medico=nombre_medico,
                        medication=prescripcion,
                        special_instructions=recomendaciones
                    )
                
                # Mensaje de éxito
                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.markdown("### ✅ Registro Exitoso")
                st.markdown(f"""
                El paciente **{nombre_paciente}** ha sido registrado correctamente en el sistema.
                
                **Información guardada:**
                - Correo: {correo_paciente}
                - Teléfono: {COUNTRY_CODES[indicativo]} {telefono}
                - Médico tratante: {nombre_medico}
                - Fecha de registro: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                """)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Mostrar resultado de la llamada
                if resultado_llamada["success"]:
                    st.success(resultado_llamada["message"])
                    st.info("💬 El agente conversacional de ElevenLabs contactará al paciente para confirmar la información y proporcionar las instrucciones médicas.")
                else:
                    st.warning(resultado_llamada["message"])
                
                st.balloons()
                
                # Botón para limpiar formulario
                if st.button("➕ Registrar Nuevo Paciente"):
                    st.rerun()
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p>🏥 Sistema de Seguimiento Médico | Adulto Mayor Chile</p>
            <p style="font-size: 0.85rem; color: #9ca3af;">
                Plataforma desarrollada para mejorar la atención y seguimiento de pacientes
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

