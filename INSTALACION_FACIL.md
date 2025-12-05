# AI Image Describer para NVDA

## Instalacion Super Facil (Para Cualquier Usuario)

### Paso 1: Instalar el Complemento
1. Asegurate de que NVDA este en ejecucion
2. Haz doble clic en: **aiImageDescriber-0.1.0.nvda-addon**
3. NVDA preguntara si deseas instalarlo - presiona "Si"
4. Reinicia NVDA cuando te lo pida

### Paso 2: Primera Ejecucion (Automatico)
Cuando NVDA se reinicie, el complemento detectara automaticamente que faltan algunos componentes necesarios y te preguntara:

**"AI Image Describer necesita instalar los siguientes componentes: Pillow, requests"**

- Presiona **"Si"** para instalarlos automaticamente
- Espera 10-30 segundos mientras se descargan
- Reinicia NVDA de nuevo cuando termine

**¡Eso es todo!** Los componentes se instalaran solos.

### Paso 3: Obtener API Key (Gratis)

Necesitas una clave API de un proveedor de IA. Elige UNO:

**Opcion A: Google Gemini (GRATIS, Recomendado para empezar)**
1. Ve a: https://makersuite.google.com/app/apikey
2. Inicia sesion con tu cuenta de Google
3. Haz clic en "Create API Key"
4. Copia la clave (empieza con AIza...)

**Opcion B: OpenAI GPT-4 Vision (Mejor calidad, ~1 centavo por imagen)**
1. Ve a: https://platform.openai.com/api-keys
2. Crea una cuenta
3. Haz clic en "Create new secret key"
4. Copia la clave (empieza con sk-...)
5. Anade credito en Billing (minimo $5 USD)

### Paso 4: Configurar

1. Con NVDA abierto, presiona: **NVDA+N**
2. Ve a: **Preferencias → Configuracion**
3. Busca la categoria: **AI Image Describer**
4. Selecciona tu proveedor (Gemini u OpenAI)
5. Pega tu API key en el campo correspondiente
6. Haz clic en **"Probar conexion"**
7. Si dice "Conexion exitosa", haz clic en **"Aceptar"**

### Paso 5: ¡Usar!

**Atajos de teclado:**
- **NVDA+Shift+I** → Describir imagen donde esta el cursor
- **NVDA+Shift+S** → Capturar y describir toda la pantalla
- **NVDA+Shift+F** → Abrir una imagen desde un archivo

**Ejemplo rapido:**
1. Abre tu navegador
2. Ve a Wikipedia o cualquier pagina con imagenes
3. Navega hasta una imagen
4. Presiona **NVDA+Shift+I**
5. Espera 3-5 segundos
6. ¡Escucha la descripcion!

## Preguntas Frecuentes

**¿Necesito saber programar?**
No. Todo es automatico.

**¿Necesito instalar Python?**
No. NVDA ya tiene Python incluido.

**¿Necesito instalar algo manualmente?**
No. El complemento instala todo automaticamente.

**¿Es gratis?**
- Google Gemini: Si, gratis hasta 60 imagenes por minuto
- OpenAI: No, cuesta aproximadamente 1 centavo USD por imagen

**¿Funciona sin Internet?**
No, necesita Internet para enviar las imagenes a la IA.

**¿Mis imagenes son privadas?**
Las imagenes se envian a OpenAI o Google para procesarlas. Lee sus politicas de privacidad.

**No funciona, ¿que hago?**
1. Verifica que reiniciaste NVDA despues de instalar
2. Verifica que los componentes se instalaron (deben haberte preguntado)
3. Verifica que tu API key este configurada correctamente
4. Presiona NVDA+F1 y busca errores de "aiImageDescriber" en el log

**¿Puedo usar imagenes con texto?**
Si, ambos modelos (OpenAI y Gemini) detectan y leen texto en imagenes automaticamente.

## Solución de Problemas

**"Error: No hay un proveedor de IA configurado"**
→ Configura tu API key (Paso 4)

**"API key invalida"**
→ Verifica que copiaste bien la clave
→ Para OpenAI: verifica que tengas credito en tu cuenta

**No me pregunto sobre instalar componentes**
→ Puede que ya los tengas instalados
→ Prueba usar el complemento directamente

**Error al instalar componentes automaticamente**
→ Intenta manualmente:
1. Abre PowerShell como Administrador
2. Ejecuta: cd "C:\Program Files\NVDA"
3. Ejecuta: python -m pip install Pillow requests
4. Reinicia NVDA

## Resumen

**Para usuarios sin conocimientos tecnicos:**
1. Doble clic en el archivo .nvda-addon
2. Reinicia NVDA
3. Di "Si" cuando pregunte por componentes
4. Reinicia NVDA de nuevo
5. Obten API key (Gemini es gratis)
6. Pega la key en configuracion
7. ¡Listo! Usa NVDA+Shift+I

**Tiempo total: 5-10 minutos**

---

**Version:** 0.1.0
**Autor:** jmortizsilva
**Licencia:** GPL v2
