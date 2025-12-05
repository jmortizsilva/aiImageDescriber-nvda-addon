# AI Image Describer para NVDA

## Descripción

**AI Image Describer** es un complemento para NVDA que utiliza inteligencia artificial para describir imágenes automáticamente. Permite a usuarios ciegos y con baja visión acceder al contenido visual de imágenes en documentos, páginas web, y archivos.

### Características principales

- 🖼️ **Descripción de imágenes en documentos**: Describe imágenes en Word, navegadores, PDFs y otras aplicaciones
- 📸 **Captura de pantalla**: Captura y describe la pantalla completa o regiones específicas
- 📁 **Carga de archivos**: Abre y describe imágenes desde archivos locales
- 🤖 **Múltiples proveedores de IA**: Soporta OpenAI GPT-4 Vision y Google Gemini
- 🌍 **Multiidioma**: Descripciones en español, inglés y francés
- ⚙️ **Configurable**: Panel de configuración integrado en las preferencias de NVDA

## Requisitos

- **NVDA**: Versión 2021.1 o superior
- **Python**: Python 3.7+ (incluido con NVDA)
- **Conexión a Internet**: Requerida para las APIs de IA
- **API Key**: Necesitas una clave API de OpenAI o Google Gemini

## Instalación

### 1. Instalar el complemento

1. Descarga el archivo `.nvda-addon`
2. Abre el archivo con NVDA en ejecución
3. NVDA te preguntará si deseas instalar el complemento
4. Confirma la instalación y reinicia NVDA

### 2. Instalar dependencias

El complemento requiere las siguientes bibliotecas de Python:

```bash
pip install Pillow requests
```

**Para usuarios de NVDA instalado desde el instalador:**

1. Abre PowerShell o CMD como administrador
2. Navega al directorio de Python de NVDA:
   ```
   cd "C:\Program Files\NVDA\lib\python"
   ```
3. Instala las dependencias:
   ```
   python.exe -m pip install Pillow requests
   ```

**Para usuarios de NVDA portable:**

1. Abre PowerShell o CMD
2. Navega al directorio de tu NVDA portable
3. Ejecuta:
   ```
   .\python.exe -m pip install Pillow requests
   ```

### 3. Configurar API Keys

Para usar el complemento, necesitas obtener una API key de uno de estos proveedores:

#### OpenAI (GPT-4 Vision)

1. Visita: https://platform.openai.com/api-keys
2. Crea una cuenta o inicia sesión
3. Genera una nueva API key
4. Copia la clave (empieza con `sk-...`)

**Costo aproximado**: $0.01 por imagen (varía según tamaño y detalle)

#### Google Gemini

1. Visita: https://makersuite.google.com/app/apikey
2. Crea una cuenta de Google Cloud o inicia sesión
3. Genera una API key
4. Copia la clave (empieza con `AIza...`)

**Costo**: Gratuito hasta cierto límite mensual

### 4. Configurar el complemento

1. Abre NVDA
2. Ve a: NVDA → Preferencias → Configuración
3. Busca la categoría **AI Image Describer**
4. Selecciona tu proveedor de IA (OpenAI o Gemini)
5. Pega tu API key en el campo correspondiente
6. Haz clic en "Probar conexión" para verificar
7. Ajusta otras opciones según prefieras
8. Guarda la configuración

## Uso

### Atajos de teclado

#### Comandos básicos (verbalizan la descripción)

| Atajo | Función |
|-------|---------|
| `NVDA+Shift+I` | Describir imagen bajo el foco o cursor |
| `NVDA+Shift+F` | Capturar y describir pantalla completa |
| `NVDA+Shift+C` | Describir imagen desde el portapapeles |
| `NVDA+Shift+L` | Cargar y describir imagen desde archivo |

#### Comandos con ventana (añadir Control para mostrar resultado en ventana)

| Atajo | Función |
|-------|---------|
| `NVDA+Shift+Control+I` | Describir imagen en foco y mostrar en ventana |
| `NVDA+Shift+Control+F` | Capturar pantalla y mostrar en ventana |
| `NVDA+Shift+Control+C` | Describir portapapeles y mostrar en ventana |
| `NVDA+Shift+Control+L` | Cargar archivo y mostrar en ventana |

#### Otros comandos

| Atajo | Función |
|-------|---------|
| `NVDA+Shift+H` | Mostrar ayuda rápida |
| `NVDA+Shift+S` | Abrir configuración del complemento |

**Nota**: Los comandos básicos verbalizan el resultado. Para ver la descripción en una ventana donde puedes copiarla o revisarla con más detalle, añade la tecla `Control` a cualquier comando básico.

### Ejemplos de uso

#### 1. Describir una imagen en una página web

1. Navega con NVDA hasta una imagen en el navegador
2. Presiona `NVDA+Shift+I` (verbaliza) o `NVDA+Shift+Control+I` (ventana)
3. Espera unos segundos mientras se procesa
4. NVDA leerá la descripción de la imagen

#### 2. Describir una captura de pantalla

1. Presiona `NVDA+Shift+F` (verbaliza) o `NVDA+Shift+Control+F` (ventana)
2. NVDA capturará la pantalla completa
3. Espera mientras se procesa
4. Escucha la descripción de lo que aparece en pantalla

#### 3. Describir una imagen desde archivo

1. Presiona `NVDA+Shift+L` (verbaliza) o `NVDA+Shift+Control+L` (ventana)
2. Se abrirá un diálogo de selección de archivo
3. Navega hasta tu imagen (JPG, PNG, BMP, etc.)
4. Selecciona el archivo
5. NVDA procesará y describirá la imagen

#### 4. Describir una imagen desde el portapapeles

1. Copia una imagen al portapapeles (Ctrl+C en una aplicación)
2. Presiona `NVDA+Shift+C` (verbaliza) o `NVDA+Shift+Control+C` (ventana)
3. NVDA procesará y describirá la imagen

## Configuración

### Opciones disponibles

- **Proveedor de IA**: Elige entre OpenAI GPT-4 Vision o Google Gemini
- **API Keys**: Configura tus claves de API para cada proveedor
- **Nivel de detalle**:
  - Bajo: Descripciones más rápidas y concisas
  - Normal: Balance entre velocidad y detalle
  - Alto: Descripciones más detalladas (más lento)
- **Idioma**: Español, inglés o francés para las descripciones
- **Anunciar procesamiento**: Anuncia cuando se está procesando una imagen

## Solución de problemas

### "Error: No hay un proveedor de IA configurado"

- Verifica que hayas configurado una API key válida
- Abre la configuración y prueba la conexión

### "Error: API key inválida"

- Verifica que hayas copiado correctamente la API key
- Asegúrate de que la API key tenga permisos activos
- Para OpenAI, verifica que tu cuenta tenga créditos

### "Error de conexión"

- Verifica tu conexión a Internet
- Verifica que no haya un firewall bloqueando NVDA
- Intenta más tarde si el servicio está temporalmente no disponible

### "PIL/Pillow no disponible"

- Reinstala las dependencias siguiendo los pasos de instalación
- Verifica que estés usando el Python correcto de NVDA

### El complemento no describe imágenes en Word

- Asegúrate de que la imagen esté seleccionada
- Intenta usar la captura de pantalla (`NVDA+Shift+F`) como alternativa
- Algunas imágenes incrustadas pueden requerir métodos especiales

## Privacidad y seguridad

- Las imágenes se envían a servidores de OpenAI o Google para procesamiento
- No se almacenan imágenes localmente después del procesamiento
- Tu API key se guarda en la configuración de NVDA (no encriptada)
- Revisa las políticas de privacidad de OpenAI/Google para más información

## Limitaciones conocidas

- Requiere conexión a Internet para funcionar
- El procesamiento puede tardar varios segundos por imagen
- La calidad de las descripciones depende del proveedor de IA
- Algunos formatos de imagen no están soportados
- La extracción de imágenes de ciertos controles puede fallar

## Desarrollo y contribuciones

Este complemento es código abierto. Reporta problemas o contribuye en:
https://github.com/jmortizsilva/aiImageDescriber

## Licencia

GPL v2 - Ver LICENSE para más detalles

## Créditos

Desarrollado por: jmortizsilva

Agradecimientos especiales:
- Comunidad de NVDA
- NV Access
- Comunidad de desarrolladores de complementos NVDA

## Changelog

### Versión 0.1.0 (Diciembre 2025)
- Versión inicial
- Soporte para OpenAI GPT-4 Vision
- Soporte para Google Gemini
- Captura de pantalla completa
- Carga de imágenes desde archivo
- Panel de configuración integrado
- Descripción de imágenes en documentos

## Contacto

Para preguntas, sugerencias o reporte de errores:
- GitHub: https://github.com/jmortizsilva/aiImageDescriber/issues
- Email: [tu-email]

---

**¡Disfruta accediendo al contenido visual con AI Image Describer!** 🎉
