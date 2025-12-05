# Script para crear paquete .nvda-addon
# Este script empaqueta el complemento en un archivo instalable para NVDA

import zipfile
import os
from pathlib import Path

print("="*60)
print("Creando paquete AI Image Describer para NVDA")
print("="*60)
print()

# Directorio base del proyecto
base_dir = Path(__file__).parent
addon_name = "aiImageDescriber-0.1.0.nvda-addon"

# Eliminar archivo anterior si existe
if os.path.exists(addon_name):
    os.remove(addon_name)
    print(f"Eliminando version anterior...")
    print()

# Crear archivo ZIP con compresion
print(f"Creando archivo: {addon_name}")
with zipfile.ZipFile(addon_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    
    # Agregar manifest.ini en la raiz
    manifest_path = base_dir / 'manifest.ini'
    if manifest_path.exists():
        print("  + manifest.ini")
        zipf.write(manifest_path, 'manifest.ini')
    else:
        print("ERROR: No se encuentra manifest.ini")
        exit(1)
    
    # Agregar todo el contenido de addon/
    addon_dir = base_dir / 'addon'
    if not addon_dir.exists():
        print("ERROR: No se encuentra el directorio addon/")
        exit(1)
    
    for root, dirs, files in os.walk(addon_dir):
        # Ignorar directorios de cache
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        for file in files:
            # Ignorar archivos de cache de Python
            if file.endswith('.pyc'):
                continue
            
            file_path = Path(root) / file
            # IMPORTANTE: La ruta en el ZIP debe ser relativa desde addon_dir
            # SIN el prefijo 'addon/', para que quede: globalPlugins/..., doc/...
            arcname = file_path.relative_to(addon_dir).as_posix()
            print(f"  + {arcname}")
            zipf.write(file_path, arcname)

print()
print("="*60)
print(f"✓ Paquete creado exitosamente: {addon_name}")
print("="*60)
print()
print("Para instalar:")
print("1. Asegúrate de tener NVDA en ejecución")
print("2. Haz doble clic en el archivo .nvda-addon")
print("3. Confirma la instalación")
print("4. Reinicia NVDA")
print()
print("El complemento instalará automáticamente Pillow y requests")
print("cuando lo uses por primera vez.")
print()
