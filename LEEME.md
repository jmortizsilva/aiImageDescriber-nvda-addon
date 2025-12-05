# Contenido del Proyecto

## 📦 Para Usuarios Finales

**aiImageDescriber-0.1.0.nvda-addon** 
→ Este es el archivo que debes compartir e instalar
→ 17.85 KB, instalación 100% automática

**INSTALACION_FACIL.md**
→ Guía paso a paso para usuarios sin conocimientos técnicos
→ Incluye cómo obtener API keys gratis

## 📚 Documentación

**README.md** - Visión general del proyecto y características

**QUICKSTART.md** - Guía de inicio rápido (5 minutos)

**ARCHITECTURE.md** - Documentación técnica detallada para desarrolladores

**PROJECT_SUMMARY.md** - Resumen completo del proyecto

## 🛠️ Para Desarrollo

**addon/** - Carpeta con el código fuente del complemento
  - globalPlugins/aiImageDescriber/ - Código principal
  - doc/es/ - Documentación incluida en el addon

**build_addon.py** - Script para crear el .nvda-addon desde el código

**buildVars.py** - Variables de construcción del complemento

**manifest.ini** - Metadatos del complemento (nombre, versión, autor)

**requirements.txt** - Lista de dependencias Python (referencia)

**.gitignore** - Archivos a ignorar en Git

## 🚀 Uso Rápido

**Para compartir con usuarios:**
1. Envía solo: `aiImageDescriber-0.1.0.nvda-addon`
2. Adjunta opcionalmente: `INSTALACION_FACIL.md`

**Para modificar el código:**
1. Edita archivos en `addon/`
2. Ejecuta: `python build_addon.py`
3. Se genera nuevo .nvda-addon

**Para desarrolladores:**
- Lee `ARCHITECTURE.md` para entender la estructura
- Lee `PROJECT_SUMMARY.md` para ver el estado completo
