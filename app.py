import streamlit as st
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
    page_icon="⚕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados para un diseño elegante y formal
st.markdown("""
    <style>
    /* Estilos generales */
    .main {
        background-color: #f3f4f6;
    }
    
    /* Contenedor principal del formulario */
    .block-container {
        max-width: 800px;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Eliminar padding superior de Streamlit */
    .main .block-container {
        padding-top: 1rem;
    }
    
    /* Encabezado principal */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-container h1 {
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .header-title {
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .header-container p {
        color: white !important;
        font-size: 0.75rem !important;
        text-align: center;
        margin-top: 0.2rem;
        margin-bottom: 0;
    }
    
    .header-subtitle {
        color: white !important;
        font-size: 0.75rem !important;
        text-align: center;
        margin-top: 0.2rem;
    }
    
    /* Tarjetas de sección */
    .section-card {
        background: white;
        padding: 0.8rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        margin-bottom: 0.8rem;
    }
    
    .section-title {
        color: #667eea;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.3rem;
    }
    
    /* Botones */
    .stButton>button {
        background: linear-gradient(135deg, #5b7cfa 0%, #4c63d2 100%);
        color: white;
        font-weight: 600;
        padding: 1rem 2rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 12px rgba(91, 124, 250, 0.4);
        transition: all 0.3s ease;
        width: 100%;
        font-size: 1.1rem;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #4c63d2 0%, #3d4fb8 100%);
        box-shadow: 0 6px 16px rgba(91, 124, 250, 0.5);
        transform: translateY(-2px);
    }
    
    /* Inputs */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
        background-color: #f9fafb;
        font-size: 0.95rem;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #5b7cfa;
        box-shadow: 0 0 0 3px rgba(91, 124, 250, 0.1);
        background-color: white;
    }
    
    /* Espaciado entre campos */
    .stTextInput, .stTextArea, .stSelectbox {
        margin-bottom: 1rem;
    }
    
    /* Mensajes de éxito y error */
    .success-message {
        background-color: #d1fae5;
        color: #065f46;
        padding: 0.6rem;
        border-radius: 8px;
        border-left: 4px solid #10b981;
        margin: 0.5rem 0;
    }
    
    .error-message {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 0.6rem;
        border-radius: 8px;
        border-left: 4px solid #ef4444;
        margin: 0.5rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        padding: 1rem 0;
        margin-top: 1.5rem;
        border-top: 1px solid #e5e7eb;
    }
    
    /* Labels */
    label {
        color: #374151;
        font-weight: 500;
        font-size: 0.85rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f3f4f6;
    }
    
    /* Reducir espacios y tamaños de títulos */
    h2 {
        font-size: 1.1rem !important;
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
    }
    
    h3 {
        font-size: 1rem !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.2rem !important;
    }
    
    .stMarkdown {
        margin-bottom: 0.2rem !important;
    }
    
    /* Eliminar espacios extra en labels */
    label {
        margin-bottom: 0.2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Códigos de país para teléfonos
COUNTRY_CODES = {
    "Chile (+56)": "+56",
    "Argentina (+54)": "+54",
    "Perú (+51)": "+51",
    "Colombia (+57)": "+57",
    "México (+52)": "+52",
    "España (+34)": "+34",
    "Estados Unidos (+1)": "+1",
    "Brasil (+55)": "+55",
    "Uruguay (+598)": "+598",
    "Paraguay (+595)": "+595",
    "Bolivia (+591)": "+591",
    "Ecuador (+593)": "+593",
    "Venezuela (+58)": "+58",
}

def validar_telefono(telefono):
    """Valida que el teléfono contenga solo números"""
    return telefono.isdigit() and len(telefono) >= 7 and len(telefono) <= 15

def hacer_llamada_elevenlabs(numero_telefono, nombre_paciente="", nombre_medico="", medication="", dosage="", special_instructions=""):
    """
    Realiza una llamada saliente (outbound) usando ElevenLabs con variables dinámicas
    
    Args:
        numero_telefono: Número completo con indicativo (ej: +573102095609)
        nombre_paciente: Nombre del paciente para personalizar la llamada
        nombre_medico: Nombre del médico tratante (opcional)
        medication: Prescripción médica / Medicación (opcional)
        dosage: Dosificación del medicamento (opcional)
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
                "message": "Credenciales de ElevenLabs incompletas. Verifica el archivo .env"
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
        
        # Agregar dosage si está disponible
        if dosage:
            dynamic_variables["dosage"] = dosage
        
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
            "message": f"Llamada iniciada exitosamente al número {numero_telefono}",
            "response": response
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error al realizar la llamada: {str(e)}"
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
            <h1 class="header-title">Sistema de Seguimiento Médico</h1>
            <p class="header-subtitle">Plataforma de Gestión Integral para Pacientes y Profesionales de la Salud</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Mostrar registros si se solicita
    if 'mostrar_registros' in st.session_state and st.session_state.mostrar_registros:
        st.markdown("---")
        st.markdown("## Historial de Registros")
        
        if os.path.exists('registros_pacientes.json'):
            with open('registros_pacientes.json', 'r', encoding='utf-8') as f:
                registros = json.load(f)
                
            if registros:
                for idx, registro in enumerate(reversed(registros), 1):
                    with st.expander(f"Paciente: {registro['nombre']} - {registro['fecha_registro']}", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Teléfono:** {registro.get('telefono_completo', 'N/A')}")
                            st.markdown(f"**Medicación:** {registro.get('medicacion', 'N/A')}")
                        with col2:
                            st.markdown(f"**Doctor:** {registro.get('nombre_medico', 'N/A')}")
                            st.markdown(f"**Dosificación:** {registro.get('dosificacion', 'N/A')}")
                            st.markdown(f"**Fecha:** {registro['fecha_registro']}")
                        
                        if registro.get('recomendaciones'):
                            st.markdown("**Instrucciones Especiales:**")
                            st.info(registro['recomendaciones'])
            else:
                st.info("No hay registros disponibles.")
        else:
            st.info("No hay registros disponibles.")
        
        if st.button("← Cerrar Registros"):
            st.session_state.mostrar_registros = False
            st.rerun()
        
        st.markdown("---")
    
    # Formulario principal con diseño limpio
    with st.container():
        # Nombre del Paciente
        nombre_paciente = st.text_input(
            "Nombre del Paciente",
            placeholder="Ingrese el nombre completo del paciente",
            label_visibility="visible"
        )
        
        # Nombre del Doctor
        nombre_medico = st.text_input(
            "Nombre del Doctor",
            placeholder="Ingrese el nombre del doctor tratante",
            label_visibility="visible"
        )
        
        # Número de Teléfono
        st.markdown('<p style="font-size: 0.85rem; font-weight: 500; color: #374151; margin-bottom: 0.3rem;">Número de Teléfono</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            indicativo = st.selectbox(
                "País",
                options=list(COUNTRY_CODES.keys()),
                label_visibility="collapsed"
            )
        with col2:
            telefono = st.text_input(
                "Teléfono",
                placeholder="300 123 4567",
                label_visibility="collapsed"
            )
        
        # Mostrar formato esperado
        if telefono:
            telefono_completo = f"{COUNTRY_CODES[indicativo]} {telefono}"
            st.markdown(f'<p style="color: #6b7280; font-size: 0.75rem; margin-top: -0.5rem;">Formato: {telefono_completo} (debe incluir código de país)</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p style="color: #6b7280; font-size: 0.75rem; margin-top: -0.5rem;">Formato: {COUNTRY_CODES[indicativo]} 300 123 4567 (debe incluir código de país)</p>', unsafe_allow_html=True)
        
        # Medicación Prescrita y Dosificación en dos columnas
        col1, col2 = st.columns(2)
        with col1:
            medicacion = st.text_input(
                "Medicación Prescrita",
                placeholder="Ej., Amoxicilina"
            )
        with col2:
            dosificacion = st.text_input(
                "Dosificación",
                placeholder="Ej., 500mg cada 8 horas"
            )
        
        # Instrucciones Especiales
        recomendaciones = st.text_area(
            "Instrucciones Especiales",
            placeholder="Notas adicionales para el paciente...",
            height=120
        )
    
    if st.button("📞 Iniciar Llamada de Seguimiento", use_container_width=True):
        # Validaciones (solo de formato, no obligatorias)
        errores = []
        
        # Validación opcional de formato de teléfono
        if telefono and not validar_telefono(telefono):
            errores.append("El número de teléfono debe contener solo dígitos (7-15)")
        
        # Mostrar errores o guardar
        if errores:
            st.markdown('<div class="error-message">', unsafe_allow_html=True)
            st.markdown("### Errores en el formulario:")
            for error in errores:
                st.markdown(f"- {error}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Combinar medicación y dosificación
            prescripcion_completa = f"{medicacion} - {dosificacion}" if medicacion and dosificacion else (medicacion or dosificacion or "")
            
            # Guardar registro
            datos_registro = {
                "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nombre": nombre_paciente,
                "nombre_medico": nombre_medico,
                "indicativo": COUNTRY_CODES[indicativo],
                "telefono": telefono,
                "telefono_completo": f"{COUNTRY_CODES[indicativo]} {telefono}",
                "medicacion": medicacion,
                "dosificacion": dosificacion,
                "prescripcion": prescripcion_completa,
                "recomendaciones": recomendaciones
            }
            
            guardar_registro(datos_registro)
            
            # Realizar llamada automática con ElevenLabs
            telefono_para_llamar = f"{COUNTRY_CODES[indicativo]}{telefono}"
            
            with st.spinner('Iniciando llamada al paciente...'):
                resultado_llamada = hacer_llamada_elevenlabs(
                    numero_telefono=telefono_para_llamar,
                    nombre_paciente=nombre_paciente,
                    nombre_medico=nombre_medico,
                    medication=medicacion,
                    dosage=dosificacion,
                    special_instructions=recomendaciones
                )
            
            # Mensaje de éxito
            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.markdown("### ✓ Llamada Iniciada")
            mensaje_detalles = f"""
            La llamada de seguimiento para **{nombre_paciente}** ha sido iniciada correctamente.
            
            **Detalles:**
            - Teléfono: {COUNTRY_CODES[indicativo]} {telefono}"""
            
            if nombre_medico:
                mensaje_detalles += f"\n            - Doctor: {nombre_medico}"
            
            mensaje_detalles += f"""
            - Medicación: {medicacion or 'No especificada'}
            - Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            """
            
            st.markdown(mensaje_detalles)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Mostrar resultado de la llamada
            if resultado_llamada["success"]:
                st.success(resultado_llamada["message"])
                st.info("El agente conversacional contactará al paciente para proporcionar las instrucciones médicas.")
            else:
                st.warning(resultado_llamada["message"])
            
            # Botón para limpiar formulario
            if st.button("+ Nuevo Paciente"):
                st.rerun()
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p>Sistema de Seguimiento Médico | Adulto Mayor</p>
            <p style="font-size: 0.85rem; color: #9ca3af;">
                Plataforma desarrollada para mejorar la atención y seguimiento de pacientes
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

