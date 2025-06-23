# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS # Importa Flask-CORS para manejar solicitudes de origen cruzado
import os
import sys

import json
import requests # Asegúrate de que requests esté importado

# Inicializa la aplicación Flask
app = Flask(__name__)
# Habilita CORS para permitir solicitudes desde tu frontend (ajusta según sea necesario para la seguridad en producción)
CORS(app)

# Variable global para simular la configuración de Firebase
# En un entorno real de Canvas, __app_id y __firebase_config se inyectarían automáticamente.
# Para pruebas locales, proporcionamos valores predeterminados.
app_id = os.environ.get('__APP_ID', 'default-app-id')
firebase_config_str = os.environ.get('__FIREBASE_CONFIG', '{}')
firebase_config = json.loads(firebase_config_str)

@app.route('/')
def serve_frontend():
    """
    Sirve el archivo HTML principal del frontend.
    """
    try:
        return send_from_directory('.', 'index.html')
    except FileNotFoundError:
        return jsonify({
            "status": "healthy", 
            "message": "API de pesca con IA funcionando!",
            "note": "Frontend no encontrado. Asegúrate de que index.html esté en la raíz del proyecto."
        })

@app.route('/health')
def health_check():
    """
    Endpoint de verificación de estado.
    Útil para comprobar si la aplicación está funcionando.
    """
    return jsonify({
        "status": "healthy", 
        "message": "API de pesca con IA funcionando!",
        "app_id": app_id,
        "has_firebase_config": bool(firebase_config)
    })

@app.route('/api/query', methods=['POST'])
def handle_query():
    """
    Endpoint principal para recibir consultas y responder con IA.
    """
    try:
        # Obtener los datos JSON de la solicitud
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "Falta el parámetro 'query' en el cuerpo de la solicitud JSON."}), 400

        user_query = data['query']
        print(f"Consulta recibida: {user_query}")

        # Validar que la consulta no esté vacía
        if not user_query.strip():
            return jsonify({"error": "La consulta no puede estar vacía."}), 400

        # ** Lógica para llamar al modelo de IA (Gemini 2.0 Flash) **
        # La clave API se manejará automáticamente en el entorno de Canvas.
        # Para pruebas locales, si necesitas una clave, la configurarías aquí
        # o como una variable de entorno.
        api_key = os.environ.get('GEMINI_API_KEY', "")
        
        # Si no hay API key, retornar una respuesta simulada para pruebas
        if not api_key:
            return jsonify({
                "response": f"🎣 Respuesta simulada para: '{user_query}'\n\n"
                           "Esta es una respuesta de prueba. Para obtener respuestas reales de IA, "
                           "configura la variable de entorno GEMINI_API_KEY con tu clave de API de Google Gemini.\n\n"
                           "Mientras tanto, aquí tienes algunos consejos generales de pesca:\n"
                           "• Las mejores horas suelen ser al amanecer y al atardecer\n"
                           "• Observa el clima: días nublados pueden ser excelentes\n"
                           "• La paciencia es clave en la pesca\n"
                           "• Mantén tu equipo en buen estado"
            })

        # Construir el payload para la API de Gemini
        chat_history = []
        # Agregar contexto especializado en pesca
        system_prompt = """Eres un experto en pesca con años de experiencia. Proporciona consejos prácticos, 
        específicos y útiles sobre pesca. Incluye información sobre técnicas, equipos, ubicaciones, 
        condiciones climáticas, especies de peces, cebos, y cualquier otro aspecto relacionado con la pesca. 
        Mantén un tono amigable y profesional. Si la pregunta no está relacionada con pesca, 
        redirige amablemente la conversación hacia temas de pesca."""
        
        chat_history.append({"role": "user", "parts": [{"text": f"{system_prompt}\n\nPregunta del usuario: {user_query}"}]})

        payload = {
            "contents": chat_history,
            "generationConfig": {
                "responseMimeType": "text/plain",
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }

        # URL de la API de Gemini para gemini-2.0-flash
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

        # Realizar la llamada a la API de Gemini
        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status() # Lanza una excepción para códigos de estado de error (4xx o 5xx)

        result = response.json()

        # Extraer la respuesta del modelo
        ai_response_text = "No se pudo obtener una respuesta de la IA."
        if result and result.get('candidates') and len(result['candidates']) > 0 and \
           result['candidates'][0].get('content') and result['candidates'][0]['content'].get('parts') and \
           len(result['candidates'][0]['content']['parts']) > 0:
            ai_response_text = result['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"Estructura de respuesta inesperada de Gemini: {result}")
            ai_response_text = "La IA no pudo generar una respuesta en este momento. Intenta reformular tu pregunta."

        # Devolver la respuesta de la IA
        return jsonify({"response": ai_response_text})

    except requests.exceptions.Timeout:
        print("Timeout al llamar a la API de Gemini")
        return jsonify({"error": "La solicitud tardó demasiado tiempo. Intenta de nuevo."}), 504
    except requests.exceptions.RequestException as e:
        # Manejo de errores de red o de la API de Gemini
        print(f"Error al llamar a la API de Gemini: {e}")
        return jsonify({"error": f"Error en el servicio de IA: {str(e)}"}), 500
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        return jsonify({"error": "Error al procesar la respuesta de la IA."}), 500
    except Exception as e:
        # Manejo de cualquier otro error inesperado
        print(f"Error inesperado: {e}")
        return jsonify({"error": f"Un error inesperado ocurrió: {str(e)}"}), 500

@app.route('/<path:path>')
def serve_static_files(path):
    """
    Sirve archivos estáticos o redirige al frontend para SPA routing.
    """
    try:
        # Si el archivo existe, lo sirve
        if os.path.exists(path):
            return send_from_directory('.', path)
        # Si no existe, sirve el index.html (para Single Page Applications)
        return send_from_directory('.', 'index.html')
    except FileNotFoundError:
        return jsonify({"error": "Archivo no encontrado"}), 404

@app.errorhandler(404)
def not_found(error):
    """
    Maneja errores 404 - Página no encontrada
    """
    return jsonify({
        "error": "Endpoint no encontrado",
        "message": "Verifica la URL y método HTTP",
        "available_endpoints": {
            "GET /": "Frontend de la aplicación",
            "GET /health": "Estado de la aplicación",
            "POST /api/query": "Consultas a la IA"
        }
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """
    Maneja errores internos del servidor
    """
    return jsonify({
        "error": "Error interno del servidor",
        "message": "Ha ocurrido un error inesperado. Intenta de nuevo más tarde."
    }), 500

# Función para verificar las variables de entorno necesarias
def check_environment():
    """
    Verifica que las variables de entorno necesarias estén configuradas
    """
    required_vars = []
    warnings = []
    
    if not os.environ.get('GEMINI_API_KEY'):
        warnings.append("GEMINI_API_KEY no configurada - se usarán respuestas simuladas")
    
    if warnings:
        print("⚠️  ADVERTENCIAS DE CONFIGURACIÓN:")
        for warning in warnings:
            print(f"   - {warning}")
        print()
    
    print("✅ Aplicación iniciada correctamente")
    print(f"   - App ID: {app_id}")
    print(f"   - Puerto: {os.environ.get('PORT', 'No especificado (usará default)')}")
    print(f"   - Modo debug: {app.debug}")

# Inicializar verificaciones al importar el módulo
if __name__ != '__main__':
    check_environment()

# El bloque if __name__ == '__main__': se elimina para que Gunicorn maneje el inicio.
# La instancia 'app' de Flask está ahora directamente disponible para Gunicorn.