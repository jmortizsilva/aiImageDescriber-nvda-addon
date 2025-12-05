# 🚀 Guía de Inicio Rápido - AI Image Describer

## Instalación Rápida (5 minutos)

### Paso 1: Instalar dependencias
Ejecuta `install_dependencies.ps1` haciendo clic derecho → "Ejecutar con PowerShell"

O manualmente:
```powershell
cd "C:\Program Files\NVDA\lib\python"
python.exe -m pip install Pillow requests
```

### Paso 2: Instalar el complemento

**Opción A - Desarrollo/Pruebas:**
1. Copia la carpeta `addon/globalPlugins/aiImageDescriber` a:
   ```
   %APPDATA%\nvda\addons\aiImageDescriber\globalPlugins\
   ```
2. Reinicia NVDA

**Opción B - Paquete completo:**
1. Empaqueta el addon (ver sección de empaquetado)
2. Instala el archivo `.nvda-addon` generado

### Paso 3: Obtener API Key

**Para OpenAI (Recomendado):**
1. Ve a https://platform.openai.com/api-keys
2. Crea una cuenta o inicia sesión
3. Click en "Create new secret key"
4. Copia la key (empieza con `sk-...`)
5. **Importante**: Añade crédito a tu cuenta en Billing

**Para Gemini (Alternativa gratuita):**
1. Ve a https://makersuite.google.com/app/apikey
2. Inicia sesión con tu cuenta de Google
3. Click en "Get API Key"
4. Copia la key (empieza con `AIza...`)

### Paso 4: Configurar NVDA

1. Abre NVDA
2. Presiona `NVDA+N` → Preferencias → Configuración
3. Busca "AI Image Describer"
4. Selecciona tu proveedor (OpenAI o Gemini)
5. Pega tu API key
6. Click en "Probar conexión"
7. Si la prueba es exitosa, guarda la configuración

## ✅ Prueba Rápida

### Probar con una imagen de internet:
1. Abre tu navegador
2. Ve a cualquier sitio con imágenes (ej: wikipedia.org)
3. Navega hasta una imagen con NVDA
4. Presiona `NVDA+Shift+I`
5. Espera 3-5 segundos
6. ¡Escucha la descripción!

### Probar con captura de pantalla:
1. Abre cualquier programa con contenido visual
2. Presiona `NVDA+Shift+S`
3. Espera unos segundos
4. NVDA describirá lo que ve en la pantalla

### Probar con un archivo:
1. Presiona `NVDA+Shift+F`
2. Selecciona una foto de tu computadora
3. Espera la descripción

## ⌨️ Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| `NVDA+Shift+I` | Describir imagen en el foco |
| `NVDA+Shift+S` | Capturar pantalla completa |
| `NVDA+Shift+F` | Abrir imagen desde archivo |
| `NVDA+Shift+Alt+I` | Abrir configuración |

## 🔧 Solución de Problemas Rápida

**"No hay un proveedor de IA configurado"**
→ Configura tu API key en las preferencias

**"API key inválida"**
→ Verifica que copiaste correctamente la key
→ Para OpenAI: verifica que tengas crédito en tu cuenta

**"Error de conexión"**
→ Verifica tu conexión a internet
→ Verifica que no haya firewall bloqueando NVDA

**"PIL no disponible"**
→ Ejecuta `install_dependencies.ps1` de nuevo

## 💰 Costos Aproximados

**OpenAI GPT-4 Vision:**
- ~$0.01 por imagen (1 centavo USD)
- Calidad: Excelente
- Requiere: Cuenta con crédito

**Google Gemini:**
- Gratis hasta 60 peticiones/minuto
- Calidad: Muy buena
- Requiere: Solo cuenta de Google

## 📝 Consejos de Uso

1. **Para imágenes complejas**: Usa nivel de detalle "Alto" en configuración
2. **Para velocidad**: Usa nivel "Bajo"
3. **Para imágenes con texto**: Ambos modelos detectan texto automáticamente
4. **Para capturas de pantalla**: Funciona mejor con ventanas no muy cargadas

## 🆘 Necesitas Ayuda?

- Issues: https://github.com/jmortizsilva/aiImageDescriber/issues
- Documentación completa: Ver `addon/doc/es/readme.md`

## 🎉 ¡Listo!

Ahora puedes acceder al contenido visual con solo presionar un atajo de teclado.

---

**Tiempo estimado de configuración**: 5-10 minutos
**Dificultad**: ⭐⭐☆☆☆ Fácil
