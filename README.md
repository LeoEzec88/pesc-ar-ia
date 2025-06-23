# 🎣 Pesc-Ar-Ia - Asistente Inteligente de Pesca

Una aplicación web moderna que utiliza inteligencia artificial para proporcionar recomendaciones personalizadas de pesca, análisis de condiciones climáticas en tiempo real y consejos expertos para pescadores.

## ✨ Características Principales

### 🤖 Asistente IA de Pesca
- Chat interactivo con IA especializada en pesca
- Recomendaciones personalizadas basadas en ubicación y condiciones
- Análisis de patrones de pesca y comportamiento de peces
- Respuestas en tiempo real con formato mejorado

### 🌤️ Condiciones Climáticas en Tiempo Real
- Integración con OpenWeatherMap API
- Detección automática de ubicación (GPS)
- Análisis de condiciones óptimas para pesca
- Recomendaciones basadas en clima actual

### 🎯 Selector Inteligente de Carnadas
- Recomendaciones de carnadas por tipo de pesca:
  - Spinning
  - Pesca con mosca
  - Pesca de fondo
  - Trolling
  - Surf fishing
- Análisis IA de carnadas naturales y artificiales
- Consejos sobre cuándo y cómo usar cada carnada

### 🗺️ Características Adicionales
- Mapas inteligentes de spots de pesca
- Análisis predictivo de actividad de peces
- Diario digital de pescas
- Tutor interactivo de técnicas de pesca

## 🚀 Tecnologías Utilizadas

### Frontend
- **HTML5** con diseño responsive
- **CSS3** con gradientes, animaciones y glassmorphism
- **JavaScript** vanilla para interactividad
- **OpenWeatherMap API** para datos climáticos

### Backend (Ya implementado)
- **Flask** (Python 3.11.11) para API REST
- **Google Gemini AI** para procesamiento de consultas de pesca
- **Heroku/Railway ready** con Procfile configurado
- Endpoints implementados:
  - `GET /health` - Estado del servidor
  - `POST /api/query` - Procesamiento de consultas IA con Gemini

## 📋 Requisitos Previos

- Python 3.11.11 (especificado en `.python-version`)
- Flask y dependencias (ver `requirements.txt`)
- Google Gemini API key
- OpenWeatherMap API key (para clima)
- Acceso a internet para APIs externas
- Navegador web moderno con soporte para geolocalización

### APIs Requeridas

#### Google Gemini AI
1. Acceder a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crear API key gratuita
3. Agregar a tu archivo `.env`:
```bash
GEMINI_API_KEY=tu_api_key_de_gemini_aqui
```

#### OpenWeatherMap API
1. Registrarse en [OpenWeatherMap](https://openweathermap.org/api)
2. Obtener API key gratuita
3. Agregar a tu archivo `.env`:
```bash
WEATHER_API_KEY=tu_api_key_de_openweathermap_aqui
```

⚠️ **Importante**: El archivo `.env` ya está en `.gitignore` y no se subirá a GitHub.

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tuusuario/fishai.git
cd fishai
```

### 2. Configurar Entorno Python
```bash
# El proyecto usa Python 3.11.11 (ver .python-version)
# Si usas pyenv:
pyenv install 3.11.11
pyenv local 3.11.11

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno
Crear archivo `.env` en la raíz:
```bash
GEMINI_API_KEY=tu_api_key_de_gemini_aqui
WEATHER_API_KEY=tu_api_key_de_openweathermap_aqui
```

### 4. Ejecutar la Aplicación
```bash
# Desarrollo local
python app.py

# O usar el Procfile para simular producción
gunicorn app:app
```

### 5. Acceder a la Aplicación
- Desarrollo: `http://localhost:5000`
- Frontend: Abrir `index.html` directamente en navegador

## 📁 Estructura del Proyecto

```
fishai/
├── index.html              # Frontend principal
├── app.py                  # Backend Flask con integración Gemini
├── requirements.txt        # Dependencias Python
├── Procfile                # Configuración para deploy (Heroku/Railway)
├── .python-version         # Versión Python (3.11.11)
├── .gitignore
        .env                # Archivos a ignorar en Git
└── README.md               # Documentación del proyecto
```

## 🔧 Configuración del Backend Flask

Tu aplicación ya incluye:

```python
# app.py - Estructura implementada
from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Configuración con Gemini AI
# Variables de entorno desde .env
# Endpoints /health y /api/query implementados
```

### Archivo de configuración `.env`:
```bash
# Variables requeridas (crear tu archivo .env)
GEMINI_API_KEY=tu_api_key_de_gemini_aqui
WEATHER_API_KEY=tu_api_key_de_openweathermap_aqui
```

### Deploy Production-Ready:
- ✅ **Procfile** configurado para Heroku/Railway
- ✅ **requirements.txt** con todas las dependencias
- ✅ **Python 3.11.11** especificado en `.python-version`
- ✅ **Variables de entorno** protegidas en `.gitignore`

## 🎨 Características de Diseño

### UI/UX Moderno
- **Glassmorphism**: Efectos de vidrio esmerilado
- **Gradientes vibrantes**: Colores oceánicos
- **Animaciones fluidas**: Transiciones suaves
- **Responsive design**: Adaptable a móviles y desktop

### Elementos Interactivos
- Animaciones de peces flotantes
- Efectos hover en tarjetas
- Indicadores de carga animados
- Chat con formato mejorado

## 🔌 API Endpoints

### GET /health
```json
{
  "status": "ok",
  "message": "FishAI Backend funcionando correctamente"
}
```

### POST /api/query
**Request:**
```json
{
  "query": "¿Qué carnada usar para pejerreyes?"
}
```

**Response:**
```json
{
  "response": "Para pejerreyes te recomiendo usar lombriz colorada o mojarra como carnada natural..."
}
```

## 🌍 APIs Externas Utilizadas

### OpenWeatherMap
- **Endpoint**: `https://api.openweathermap.org/data/2.5/weather`
- **Uso**: Datos climáticos en tiempo real
- **Límite gratuito**: 1000 calls/día

### Geolocalización HTML5
- **Uso**: Detección automática de ubicación
- **Fallback**: Buenos Aires, Argentina

## 📱 Compatibilidad

### Navegadores Soportados
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Dispositivos
- 📱 Móviles (iOS/Android)
- 💻 Desktop (Windows/Mac/Linux)
- 📱 Tablets

## 🐛 Solución de Problemas

### Error de Conexión Backend
```
Error de conexión con el servidor
```
**Solución**: Verificar que Flask esté ejecutándose en puerto 5000

### Error de Geolocalización
```
Detectando ubicación...
```
**Solución**: Permitir acceso a ubicación en el navegador

### Error API Clima
```
Error obteniendo clima
```
**Solución**: Verificar API key de OpenWeatherMap

## 🚀 Deploy en Producción

### Opciones de Deploy

#### Heroku
```bash
# Tu proyecto ya está configurado con Procfile
heroku create fishai-app
heroku config:set GEMINI_API_KEY=tu_key_aqui
heroku config:set WEATHER_API_KEY=tu_key_aqui
git push heroku main
```

#### Railway
```bash
# Conectar con GitHub y agregar variables de entorno:
# GEMINI_API_KEY=tu_key_aqui
# WEATHER_API_KEY=tu_key_aqui
```

#### Render
```bash
# Conectar repositorio GitHub
# Build Command: pip install -r requirements.txt
# Start Command: python app.py
```

## 🚀 Próximas Funcionalidades

- [ ] Mapas interactivos con Google Maps
- [ ] Sistema de usuario y autenticación
- [ ] Base de datos de pescas
- [ ] Predicciones ML avanzadas
- [ ] Integración con redes sociales
- [ ] App móvil nativa
- [ ] Modo offline

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

## 👨‍💻 Autor

**Leonardo E Coronel**
- GitHub: [@<leoEzec88>](https://github.com/LeoEzec88)
- Email: lcoronel.unab@ejemplo.com

## 🙏 Agradecimientos

- OpenWeatherMap por la API climática
- Comunidad de pescadores por feedback
- Contribuidores del proyecto

---

⭐ **Si te gusta el proyecto, dale una estrella en GitHub!**

🎣 **¡Con esta app si Pesc-Ar-Ia!**