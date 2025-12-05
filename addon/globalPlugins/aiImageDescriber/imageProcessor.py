# -*- coding: UTF-8 -*-
"""
Módulo de procesamiento de imágenes
Extrae y procesa imágenes de objetos NVDA y otras fuentes
"""

import base64
import os
from io import BytesIO
from logHandler import log
import controlTypes

try:
	from PIL import Image
	PIL_AVAILABLE = True
except ImportError:
	log.warning("PIL/Pillow no disponible")
	PIL_AVAILABLE = False


class ImageProcessor:
	"""Clase para procesar y extraer imágenes"""
	
	def __init__(self):
		"""Inicializa el procesador de imágenes"""
		pass
	
	def extractFromObject(self, obj):
		"""
		Extrae imagen de un objeto NVDA
		
		Args:
			obj: Objeto NVDA
		
		Returns:
			str: Imagen en base64, o None si no se puede extraer
		"""
		try:
			# Verificar que sea un objeto gráfico
			if not self._isGraphicObject(obj):
				log.info("El objeto no es una imagen")
				return None
			
			# Intentar diferentes métodos de extracción
			imageData = None
			
			# Método 1: Desde URL (para imágenes web)
			if hasattr(obj, 'IA2Attributes') and obj.IA2Attributes:
				imageUrl = obj.IA2Attributes.get('src', None)
				if imageUrl:
					imageData = self._loadFromURL(imageUrl)
					if imageData:
						return imageData
			
			# Método 2: Desde ubicación en pantalla (captura)
			if hasattr(obj, 'location') and obj.location:
				from .imageCapture import ImageCapture
				capture = ImageCapture()
				
				left = obj.location.left
				top = obj.location.top
				right = left + obj.location.width
				bottom = top + obj.location.height
				
				imageData = capture.captureRegion(left, top, right, bottom)
				if imageData:
					return imageData
			
			# Método 3: Desde ruta de archivo local
			if hasattr(obj, 'value') and obj.value:
				if os.path.isfile(obj.value):
					imageData = self.loadFromFile(obj.value)
					if imageData:
						return imageData
			
			log.warning("No se pudo extraer imagen del objeto")
			return None
			
		except Exception as e:
			log.error(f"Error al extraer imagen de objeto: {e}", exc_info=True)
			return None
	
	def loadFromFile(self, filePath):
		"""
		Carga imagen desde archivo y la convierte a base64
		
		Args:
			filePath (str): Ruta al archivo de imagen
		
		Returns:
			str: Imagen en base64, o None si falla
		"""
		if not PIL_AVAILABLE:
			return None
		
		try:
			# Verificar que el archivo existe
			if not os.path.isfile(filePath):
				log.error(f"Archivo no encontrado: {filePath}")
				return None
			
			# Cargar imagen
			image = Image.open(filePath)
			
			# Convertir a base64
			return self._imageToBase64(image)
			
		except Exception as e:
			log.error(f"Error al cargar imagen desde archivo: {e}", exc_info=True)
			return None
	
	def _loadFromURL(self, url):
		"""
		Descarga imagen desde URL y la convierte a base64
		
		Args:
			url (str): URL de la imagen
		
		Returns:
			str: Imagen en base64, o None si falla
		"""
		if not PIL_AVAILABLE:
			return None
		
		try:
			import requests
			from requests.adapters import HTTPAdapter
			from urllib3.util.retry import Retry
			
			# Configurar sesión con reintentos
			session = requests.Session()
			retry = Retry(total=3, backoff_factor=0.3)
			adapter = HTTPAdapter(max_retries=retry)
			session.mount('http://', adapter)
			session.mount('https://', adapter)
			
			# Descargar imagen
			headers = {
				'User-Agent': 'NVDA-AIImageDescriber/1.0'
			}
			response = session.get(url, headers=headers, timeout=10)
			response.raise_for_status()
			
			# Cargar imagen desde bytes
			image = Image.open(BytesIO(response.content))
			
			return self._imageToBase64(image)
			
		except ImportError:
			log.warning("requests no disponible. No se pueden descargar imágenes de URLs")
			return None
		except Exception as e:
			log.error(f"Error al descargar imagen desde URL: {e}", exc_info=True)
			return None
	
	def _imageToBase64(self, image, format="PNG"):
		"""
		Convierte imagen PIL a base64
		
		Args:
			image: Imagen PIL
			format (str): Formato de salida
		
		Returns:
			str: Imagen en base64
		"""
		try:
			# Optimizar tamaño
			max_size = 2048
			if image.width > max_size or image.height > max_size:
				image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
			
			# Convertir a bytes
			buffered = BytesIO()
			
			if format.upper() == "JPEG":
				if image.mode == "RGBA":
					image = image.convert("RGB")
				image.save(buffered, format=format, quality=85, optimize=True)
			else:
				image.save(buffered, format=format, optimize=True)
			
			# Codificar en base64
			img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
			
			return img_base64
			
		except Exception as e:
			log.error(f"Error al convertir imagen a base64: {e}", exc_info=True)
			return None
	
	def _isGraphicObject(self, obj):
		"""
		Verifica si un objeto es una imagen
		
		Args:
			obj: Objeto NVDA
		
		Returns:
			bool: True si es imagen
		"""
		try:
			# Verificar rol
			if hasattr(obj, 'role'):
				if obj.role == controlTypes.Role.GRAPHIC:
					return True
				if obj.role == controlTypes.Role.IMAGE:
					return True
			
			# Verificar nombre de clase
			if hasattr(obj, 'windowClassName'):
				imageClasses = ['Image', 'Picture', 'Static']
				if any(cls in obj.windowClassName for cls in imageClasses):
					return True
			
			# Verificar tag HTML
			if hasattr(obj, 'HTMLAttributes'):
				htmlAttrs = obj.HTMLAttributes
				if htmlAttrs and htmlAttrs.get('tag') == 'img':
					return True
			
			return False
			
		except Exception as e:
			log.error(f"Error al verificar objeto gráfico: {e}", exc_info=True)
			return False
