# AI Image Describer - NVDA Add-on

Complemento para NVDA que describe imágenes usando inteligencia artificial (OpenAI GPT-4 Vision, Google Gemini).

## Estructura del proyecto

```
aiImageDescriber/
├── addon/
│   ├── globalPlugins/
│   │   └── aiImageDescriber/
│   │       ├── __init__.py              # Plugin principal
│   │       ├── imageCapture.py          # Captura de pantalla
│   │       ├── imageProcessor.py        # Procesamiento de imágenes
│   │       ├── apiClients/              # Clientes de APIs
│   │       │   ├── __init__.py
│   │       │   ├── openai_client.py
│   │       │   └── gemini_client.py
│   │       └── ui/                      # Interfaz de usuario
│   │           ├── __init__.py
│   │           └── settingsDialog.py
│   └── doc/
│       └── es/
│           └── readme.md                # Documentación en español
├── manifest.ini                         # Metadatos del complemento
├── buildVars.py                         # Variables de construcción
└── requirements.txt                     # Dependencias Python
```

## Desarrollo

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Empaquetar el complemento

Para crear el archivo `.nvda-addon`:

1. Descarga SCons si no lo tienes instalado
2. Ejecuta desde el directorio del proyecto:
   ```bash
   scons
   ```

O manualmente:
1. Crea un archivo ZIP con todo el contenido de `addon/`
2. Cambia la extensión de `.zip` a `.nvda-addon`

### Probar el complemento

1. Copia la carpeta `addon/globalPlugins/aiImageDescriber` a:
   - `%APPDATA%\nvda\addons\aiImageDescriber\globalPlugins\aiImageDescriber`
2. Reinicia NVDA

## Características implementadas

- ✅ Descripción de imágenes en documentos
- ✅ Captura de pantalla completa
- ✅ Carga de imágenes desde archivo
- ✅ Soporte para OpenAI GPT-4 Vision
- ✅ Soporte para Google Gemini
- ✅ Panel de configuración integrado
- ✅ Múltiples idiomas para descripciones
- ⬜ Captura de región seleccionada (por implementar)
- ⬜ Soporte para Be My Eyes (por implementar)

## Licencia

GPL v2
