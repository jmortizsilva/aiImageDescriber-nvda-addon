# Changelog - AI Image Describer

## [0.1.0] - 2025-12-05

### Añadido
- Sistema completo de comandos de teclado con esquema NVDA+Alt
- 10 comandos independientes para diferentes operaciones:
  - NVDA+Alt+I: Analizar objeto en foco (verbalizar)
  - NVDA+Alt+Shift+I: Analizar objeto en foco (ventana)
  - NVDA+Alt+S: Capturar pantalla completa (verbalizar)
  - NVDA+Alt+Shift+S: Capturar pantalla completa (ventana)
  - NVDA+Alt+C: Analizar imagen del portapapeles (verbalizar)
  - NVDA+Alt+Shift+C: Analizar imagen del portapapeles (ventana)
  - NVDA+Alt+F: Cargar imagen desde archivo (verbalizar)
  - NVDA+Alt+Shift+F: Cargar imagen desde archivo (ventana)
  - NVDA+Alt+H: Mostrar ayuda de comandos
  - NVDA+Alt+O: Abrir configuración
- Diccionario `__gestures` para mapeo de teclas
- Logging detallado para depuración

### Cambiado
- **Esquema de teclado rediseñado**: Cambiado de NVDA+Shift a NVDA+Alt para evitar conflictos
  - Eliminados conflictos con comandos nativos de NVDA (formato, TeleNVDA)
  - Comandos base (sin Shift): verbalizan descripción directamente
  - Comandos con Shift: muestran ventana con resultado
- **Límites de tokens aumentados para Gemini**:
  - Nivel LOW: 150 → 500 tokens
  - Nivel AUTO: 500 → 2000 tokens
  - Nivel HIGH: usa maxTokens por defecto (5000)
  - Llamadas a describeImage: 4000 → 6000 tokens
  - Soluciona errores con thinking tokens de Gemini
- Corrección completa de codificación UTF-8 en todo el código
- Actualización de toda la documentación con nuevos atajos

### Corregido
- Errores de indentación en métodos `_captureAndDescribe`, `_showFileDialog`, `_analyzeImageFile`
- AttributeError al ejecutar comandos (métodos no reconocidos como miembros de clase)
- Codificación incorrecta de caracteres acentuados (Ã³→ó, Ã¡→á, etc.)
- Títulos de ventanas mostrando caracteres mal codificados
- Error "MAX_TOKENS" en respuestas de Gemini

### Removido
- Sistema de doble pulsación de teclas (causaba confusión)
- Carpeta `addon/` duplicada (conflicto con `aiImageDescriber/addon/`)
- Scripts temporales de sincronización Git
- Archivos obsoletos en raíz del proyecto

### Técnico
- Estructura de código limpia con métodos de clase correctamente indentados
- Scripts de compilación Python para verificación de sintaxis
- Sistema de logs mejorado con información contextual
- Compatibilidad con NVDA 2025.3.1 y Python 3.11.9
