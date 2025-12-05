# Arquitectura Técnica - AI Image Describer

## Visión General

AI Image Describer es un complemento global (GlobalPlugin) para NVDA que integra servicios de IA para describir imágenes. El complemento captura, procesa y envía imágenes a APIs de visión computacional, retornando descripciones textuales accesibles.

## Arquitectura de Componentes

```
┌─────────────────────────────────────────────────────┐
│              NVDA (NonVisual Desktop Access)         │
│  ┌───────────────────────────────────────────────┐  │
│  │      AI Image Describer GlobalPlugin          │  │
│  │                                                │  │
│  │  ┌──────────────┐  ┌────────────────────┐    │  │
│  │  │   Scripts    │  │  Settings Panel    │    │  │
│  │  │  (Keyboard)  │  │      (GUI)         │    │  │
│  │  └──────┬───────┘  └─────────┬──────────┘    │  │
│  │         │                    │                │  │
│  │         └────────┬───────────┘                │  │
│  │                  ▼                            │  │
│  │         ┌────────────────┐                    │  │
│  │         │   Core Logic   │                    │  │
│  │         └────────┬───────┘                    │  │
│  │                  │                            │  │
│  │         ┌────────┴────────┐                   │  │
│  │         ▼                 ▼                   │  │
│  │  ┌──────────────┐  ┌──────────────┐          │  │
│  │  │   Image      │  │   Image      │          │  │
│  │  │  Capture     │  │  Processor   │          │  │
│  │  └──────┬───────┘  └──────┬───────┘          │  │
│  │         │                  │                  │  │
│  │         └────────┬─────────┘                  │  │
│  │                  ▼                            │  │
│  │         ┌────────────────┐                    │  │
│  │         │  API Clients   │                    │  │
│  │         │ ┌────┐  ┌────┐ │                    │  │
│  │         │ │ AI │  │ AI │ │                    │  │
│  │         │ └────┘  └────┘ │                    │  │
│  │         └────────┬───────┘                    │  │
│  └──────────────────┼────────────────────────────┘  │
└───────────────────┼─────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   External AI APIs    │
        │  ┌─────────────────┐  │
        │  │ OpenAI GPT-4    │  │
        │  │    Vision       │  │
        │  └─────────────────┘  │
        │  ┌─────────────────┐  │
        │  │ Google Gemini   │  │
        │  └─────────────────┘  │
        └───────────────────────┘
```

## Módulos Principales

### 1. GlobalPlugin (__init__.py)
**Responsabilidad**: Punto de entrada principal, gestión de scripts y coordinación

**Componentes clave**:
- Inicialización del plugin y carga de configuración
- Definición de scripts de teclado (decoradores @script)
- Gestión del panel de configuración
- Coordinación entre módulos
- Manejo de threading para operaciones asíncronas

**Scripts implementados**:
| Script | Gesto | Función |
|--------|-------|---------|
| `script_describeImageAtFocus` | `NVDA+Shift+I` | Describe imagen en foco |
| `script_captureFullScreen` | `NVDA+Shift+S` | Captura pantalla |
| `script_captureRegion` | `NVDA+Shift+R` | Captura región |
| `script_loadImageFromFile` | `NVDA+Shift+F` | Carga archivo |
| `script_openSettings` | `NVDA+Shift+Alt+I` | Abre config |

### 2. ImageCapture (imageCapture.py)
**Responsabilidad**: Captura de imágenes desde diferentes fuentes

**Métodos principales**:
- `captureFullScreen()`: Captura pantalla completa usando PIL.ImageGrab
- `captureActiveWindow()`: Captura ventana activa usando Win32 API
- `captureRegion(x1, y1, x2, y2)`: Captura región específica
- `captureFromClipboard()`: Obtiene imagen del portapapeles
- `_imageToBase64(image)`: Convierte PIL Image a base64

**Dependencias**:
- PIL/Pillow: Captura y manipulación de imágenes
- pywin32 (opcional): Captura avanzada de ventanas

### 3. ImageProcessor (imageProcessor.py)
**Responsabilidad**: Extracción y procesamiento de imágenes de objetos NVDA

**Métodos principales**:
- `extractFromObject(obj)`: Extrae imagen de objeto NVDA
  - Detecta tipo de objeto (ROLE_GRAPHIC, ROLE_IMAGE)
  - Extrae desde URL (imágenes web)
  - Extrae desde ubicación en pantalla
  - Extrae desde archivo local
- `loadFromFile(path)`: Carga imagen desde disco
- `_loadFromURL(url)`: Descarga imagen desde internet
- `_isGraphicObject(obj)`: Verifica si objeto es imagen

**Estrategias de extracción**:
1. **Objetos web**: Usa atributos IAccessible2 para obtener URL
2. **Objetos con ubicación**: Captura región de pantalla
3. **Referencias a archivos**: Carga desde sistema de archivos

### 4. API Clients

#### OpenAIClient (apiClients/openai_client.py)
**API**: OpenAI Chat Completions API (GPT-4 Vision)
**Modelo**: `gpt-4o` (optimizado con visión)

**Características**:
- Soporte para diferentes niveles de detalle (low/high/auto)
- Prompts personalizados por idioma
- Manejo robusto de errores HTTP
- Control de límite de tokens

**Formato de petición**:
```json
{
  "model": "gpt-4o",
  "messages": [{
    "role": "user",
    "content": [
      {"type": "text", "text": "Describe..."},
      {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
    ]
  }]
}
```

#### GeminiClient (apiClients/gemini_client.py)
**API**: Google Generative Language API
**Modelo**: `gemini-1.5-flash`

**Características**:
- Multimodal nativo (texto + imagen)
- Configuración de temperatura y tokens
- Manejo de límites de tasa
- Gratuito hasta cierto límite

**Formato de petición**:
```json
{
  "contents": [{
    "parts": [
      {"text": "Describe..."},
      {"inline_data": {"mime_type": "image/png", "data": "..."}}
    ]
  }]
}
```

### 5. Settings UI (ui/settingsDialog.py)
**Responsabilidad**: Interfaz de configuración en NVDA

**Panel de configuración** (SettingsPanel):
- Selector de proveedor (OpenAI/Gemini)
- Campos de API keys
- Botón de prueba de conexión
- Configuración de nivel de detalle
- Selector de idioma
- Opciones de anuncio

**Integración con NVDA**:
- Se registra en `NVDASettingsDialog.categoryClasses`
- Guarda configuración en `config.conf["aiImageDescriber"]`
- Validación de entrada de usuario

## Flujo de Datos

### Flujo típico: Describir imagen en foco

```
1. Usuario presiona NVDA+Shift+I
   ↓
2. script_describeImageAtFocus() es llamado
   ↓
3. Obtener objeto de foco: api.getFocusObject()
   ↓
4. Verificar configuración: _checkConfiguration()
   ↓
5. Crear thread para no bloquear NVDA
   ↓
6. _analyzeObject(obj):
   a. ImageProcessor.extractFromObject(obj)
      - Detectar tipo de objeto
      - Extraer imagen (URL, ubicación, archivo)
      - Convertir a base64
   ↓
   b. APIClient.describeImage(imageBase64)
      - Construir payload con prompt
      - Enviar petición HTTP
      - Esperar respuesta (3-10 segundos)
      - Parsear resultado
   ↓
7. ui.message(description)
   ↓
8. NVDA anuncia descripción al usuario
```

## Gestión de Configuración

**Ubicación**: `config.conf["aiImageDescriber"]`

**Estructura**:
```python
{
    "apiProvider": "openai" | "gemini",
    "openaiApiKey": "sk-...",
    "geminiApiKey": "AIza...",
    "detailLevel": "low" | "normal" | "high",
    "language": "es" | "en" | "fr",
    "announceProcessing": True | False
}
```

**Persistencia**: 
- Automática vía NVDA ConfigManager
- Guardado al cambiar en Settings Panel

## Threading y Asincronía

**Estrategia**: Threading básico con daemon threads

**Razones**:
- Las peticiones API pueden tardar 3-10 segundos
- NVDA no debe bloquearse durante el procesamiento
- Los threads daemon se terminan automáticamente al cerrar NVDA

**Implementación**:
```python
threading.Thread(
    target=self._analyzeObject,
    args=(obj,),
    daemon=True
).start()
```

**Consideraciones**:
- `ui.message()` es thread-safe
- No hay UI bloqueante
- Los errores se capturan y anuncian

## Manejo de Errores

**Niveles de manejo**:

1. **Nivel de script**: Try-catch general
2. **Nivel de módulo**: Errores específicos (PIL, requests)
3. **Nivel de API**: Errores HTTP (401, 429, etc.)

**Estrategia de logging**:
- Errores críticos: `log.error()`
- Advertencias: `log.warning()`
- Información: `log.info()`

**Comunicación al usuario**:
- Mensajes breves y claros vía `ui.message()`
- Detalles técnicos en log de NVDA

## Optimizaciones

### Procesamiento de Imágenes
- **Redimensionamiento**: Max 2048px para reducir tamaño
- **Compresión**: PNG optimizado, JPEG con quality=85
- **Conversión de formato**: RGBA → RGB cuando sea necesario

### APIs
- **Timeouts**: 30 segundos para prevenir esperas infinitas
- **Reintentos**: Configurables en requests.Session
- **Caché**: Potencial mejora futura (no implementado)

### Memoria
- **Threads daemon**: Se limpian automáticamente
- **BytesIO**: Procesamiento en memoria sin archivos temporales
- **GC**: Python maneja limpieza de imágenes PIL

## Seguridad y Privacidad

**Datos transmitidos**:
- Imágenes se envían a servidores de terceros (OpenAI/Google)
- API keys se guardan sin encriptar en config de NVDA

**Consideraciones**:
- Usuario debe ser consciente de qué imágenes envía
- API keys deben mantenerse privadas
- No hay logging de contenido de imágenes

## Extensibilidad

### Añadir nuevo proveedor de IA

1. Crear nuevo cliente en `apiClients/`:
   ```python
   class NewAPIClient:
       def __init__(self, apiKey):
           pass
       
       def describeImage(self, imageBase64, ...):
           # Implementar lógica
           pass
   ```

2. Actualizar `__init__.py`:
   - Importar cliente
   - Añadir a `_loadAPIClient()`

3. Actualizar `settingsDialog.py`:
   - Añadir opción a selector
   - Añadir campo de API key

4. Actualizar configuración:
   - Añadir key a confspec

### Añadir nuevo método de captura

1. Implementar en `imageCapture.py`:
   ```python
   def captureNewSource(self):
       # Implementar captura
       return self._imageToBase64(image)
   ```

2. Crear script en `__init__.py`:
   ```python
   @scriptHandler.script(...)
   def script_newCapture(self, gesture):
       threading.Thread(
           target=self._captureNew,
           daemon=True
       ).start()
   ```

## Testing

**Archivos de prueba**:
- `test_components.py`: Verifica importaciones y estructura
- `examples.py`: Pruebas interactivas de APIs

**Pruebas recomendadas**:
1. Importación de todos los módulos
2. Captura de pantalla funcional
3. Conexión a APIs con keys válidas
4. Descripción de imagen de prueba
5. Panel de configuración accesible

## Limitaciones Conocidas

1. **Dependencia de red**: Requiere internet funcional
2. **Latencia**: 3-10 segundos por imagen
3. **Precisión**: Depende de calidad de IA
4. **Formatos**: Algunos formatos exóticos no soportados
5. **Objetos especiales**: Algunos controles no exponen imágenes correctamente
6. **Costos**: OpenAI requiere pago por uso

## Mejoras Futuras

- [ ] Caché de descripciones
- [ ] Soporte para Be My Eyes API
- [ ] Captura de región con selector visual
- [ ] Historial de descripciones
- [ ] OCR mejorado para texto en imágenes
- [ ] Soporte offline con modelos locales
- [ ] Batch processing de múltiples imágenes
- [ ] Integración con servicios de accesibilidad del SO

## Referencias

- **NVDA Developer Guide**: https://www.nvaccess.org/files/nvda/documentation/developerGuide.html
- **OpenAI Vision API**: https://platform.openai.com/docs/guides/vision
- **Google Gemini API**: https://ai.google.dev/docs
- **PIL Documentation**: https://pillow.readthedocs.io/
