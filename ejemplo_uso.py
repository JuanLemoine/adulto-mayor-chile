"""
Script de ejemplo para probar la integración con ElevenLabs
Este script te permite probar la funcionalidad de llamadas sin usar la interfaz de Streamlit
"""

from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import os

# ============================
# CONFIGURACIÓN DE ELEVENLABS
# ============================
# Cargar credenciales desde el archivo .env
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID")
ELEVENLABS_AGENT_PHONE_NUMBER_ID = os.getenv("ELEVENLABS_AGENT_PHONE_NUMBER_ID")

# ============================

def probar_llamada_ejemplo(numero_prueba=None, nombre="Paciente de Prueba", con_variables=True):
    """
    Función de prueba para hacer una llamada con ElevenLabs
    
    Args:
        numero_prueba: Número a llamar en formato +[código][número]
        nombre: Nombre del paciente para la variable dinámica
        con_variables: Si True, envía variables dinámicas
    """
    print("🔧 Probando integración con ElevenLabs...\n")
    
    # Verificar configuración
    if not ELEVENLABS_API_KEY or ELEVENLABS_API_KEY == "tu_api_key_aqui":
        print("❌ ERROR: Debes configurar tu API Key al inicio de este archivo")
        return
    
    # Número de prueba (reemplaza con tu número)
    if not numero_prueba:
        numero_prueba = "+573102095609"  # Ejemplo: formato internacional sin espacios
    
    print(f"📞 Intentando llamar a: {numero_prueba}")
    print(f"🤖 Usando Agent ID: {ELEVENLABS_AGENT_ID}")
    print(f"📱 Phone Number ID: {ELEVENLABS_AGENT_PHONE_NUMBER_ID}")
    
    if con_variables:
        print(f"👤 Nombre del paciente: {nombre}")
        print(f"📋 Con variables dinámicas: Sí\n")
    else:
        print(f"📋 Con variables dinámicas: No\n")
    
    try:
        # Inicializar cliente
        client = ElevenLabs(
            api_key=ELEVENLABS_API_KEY,
            base_url="https://api.elevenlabs.io"
        )
        
        # Preparar parámetros de la llamada
        call_params = {
            "agent_id": ELEVENLABS_AGENT_ID,
            "agent_phone_number_id": ELEVENLABS_AGENT_PHONE_NUMBER_ID,
            "to_number": numero_prueba
        }
        
        # Agregar variables dinámicas si está habilitado
        if con_variables:
            call_params["conversation_initiation_client_data"] = {
                "dynamic_variables": {
                    "name": nombre,
                    "medication": "Paracetamol 500mg cada 8 horas por 5 días",
                    "special_instructions": "Reposo, abundantes líquidos y control en 7 días"
                }
            }
        
        # Hacer llamada según documentación oficial
        print("⏳ Iniciando llamada...")
        response = client.conversational_ai.twilio.outbound_call(**call_params)
        
        print("✅ ¡Llamada iniciada exitosamente!")
        print(f"📋 Respuesta: {response}\n")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        print("💡 Verifica:")
        print("   - API Key correcta")
        print("   - Agent ID correcto")
        print("   - Phone Number ID correcto")
        print("   - Formato del número: +[código][número] sin espacios")
        print("   - Saldo suficiente en tu cuenta de ElevenLabs")

def mostrar_formato_numeros():
    """
    Muestra ejemplos de formato correcto para números de teléfono
    """
    print("\n📱 FORMATO CORRECTO DE NÚMEROS DE TELÉFONO\n")
    print("El número debe estar en formato internacional sin espacios:")
    print("  ✅ Correcto: +56912345678")
    print("  ✅ Correcto: +573102095609")
    print("  ✅ Correcto: +5491123456789")
    print("")
    print("  ❌ Incorrecto: +56 9 1234 5678 (con espacios)")
    print("  ❌ Incorrecto: 912345678 (sin indicativo)")
    print("  ❌ Incorrecto: 56912345678 (sin +)")
    print("")
    print("Códigos de país comunes:")
    print("  🇨🇱 Chile: +56")
    print("  🇨🇴 Colombia: +57")
    print("  🇦🇷 Argentina: +54")
    print("  🇵🇪 Perú: +51")
    print("  🇲🇽 México: +52")
    print("  🇪🇸 España: +34")

if __name__ == "__main__":
    print("=" * 60)
    print("🏥 SISTEMA DE SEGUIMIENTO MÉDICO - PRUEBA DE ELEVENLABS")
    print("=" * 60)
    
    mostrar_formato_numeros()
    
    print("\n" + "=" * 60)
    respuesta = input("\n¿Deseas hacer una llamada de prueba? (s/n): ")
    
    if respuesta.lower() in ['s', 'si', 'sí', 'yes', 'y']:
        numero = input("Ingresa el número en formato +[código][número]: ")
        
        # Limpiar espacios si los hay
        numero = numero.replace(" ", "")
        
        if not numero.startswith("+"):
            print("\n❌ El número debe comenzar con +")
        else:
            # Preguntar si desea usar variables dinámicas
            print("\n¿Deseas usar variables dinámicas? (El agente usará el nombre del paciente)")
            usar_vars = input("(s/n): ")
            
            nombre_paciente = "Paciente de Prueba"
            if usar_vars.lower() in ['s', 'si', 'sí', 'yes', 'y']:
                nombre_paciente = input("Ingresa el nombre del paciente: ").strip()
                if not nombre_paciente:
                    nombre_paciente = "Paciente de Prueba"
                print("")
                probar_llamada_ejemplo(numero, nombre_paciente, con_variables=True)
            else:
                print("")
                probar_llamada_ejemplo(numero, nombre_paciente, con_variables=False)
    else:
        print("\n👋 ¡Hasta luego!")

