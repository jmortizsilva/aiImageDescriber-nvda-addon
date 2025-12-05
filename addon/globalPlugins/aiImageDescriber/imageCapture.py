# -*- coding: UTF-8 -*-
"""
Módulo de captura de imágenes
Captura pantalla completa, ventanas activas o regiones específicas
"""

import base64
from io import BytesIO
from logHandler import log

try:
	from PIL import ImageGrab, Image
	PIL_AVAILABLE = True
except ImportError:
	log.warning("PIL/Pillow no disponible. Instala con: pip install Pillow")
	PIL_AVAILABLE = False


class ImageCapture:
	"""Clase para capturar imágenes de la pantalla"""
	
	def __init__(self):
		"""Inicializa el capturador de imágenes"""
		if not PIL_AVAILABLE:
			log.error("PIL no disponible. Las funciones de captura no funcionarán.")
	
	def captureFullScreen(self):
		"""
		Captura la pantalla completa
		
		Returns:
			str: Imagen en formato base64, o None si falla
		"""
		if not PIL_AVAILABLE:
			return None
		
		try:
			# Capturar pantalla
			screenshot = ImageGrab.grab()
			
			# Convertir a base64
			return self._imageToBase64(screenshot)
			
		except Exception as e:
			log.error(f"Error al capturar pantalla: {e}", exc_info=True)
			return None
	
	def captureActiveWindow(self):
		"""
		Captura solo la ventana activa
		
		Returns:
			str: Imagen en formato base64, o None si falla
		"""
		if not PIL_AVAILABLE:
			return None
		
		try:
			# Importar módulos de Windows
			import win32gui
			import win32ui
			import win32con
			from ctypes import windll
			
			# Obtener ventana activa
			hwnd = win32gui.GetForegroundWindow()
			
			# Obtener dimensiones de la ventana
			left, top, right, bottom = win32gui.GetWindowRect(hwnd)
			width = right - left
			height = bottom - top
			
			# Capturar ventana
			hwndDC = win32gui.GetWindowDC(hwnd)
			mfcDC = win32ui.CreateDCFromHandle(hwndDC)
			saveDC = mfcDC.CreateCompatibleDC()
			
			saveBitMap = win32ui.CreateBitmap()
			saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
			saveDC.SelectObject(saveBitMap)
			
			# Copiar ventana al bitmap
			result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
			
			# Convertir a imagen PIL
			bmpinfo = saveBitMap.GetInfo()
			bmpstr = saveBitMap.GetBitmapBits(True)
			
			img = Image.frombuffer(
				'RGB',
				(bmpinfo['bmWidth'], bmpinfo['bmHeight']),
				bmpstr, 'raw', 'BGRX', 0, 1
			)
			
			# Limpiar recursos
			win32gui.DeleteObject(saveBitMap.GetHandle())
			saveDC.DeleteDC()
			mfcDC.DeleteDC()
			win32gui.ReleaseDC(hwnd, hwndDC)
			
			if result == 0:
				log.warning("PrintWindow falló, usando captura de región")
				return self.captureRegion(left, top, right, bottom)
			
			return self._imageToBase64(img)
			
		except ImportError:
			log.warning("pywin32 no disponible. Usando captura de región")
			# Fallback a captura de pantalla completa
			return self.captureFullScreen()
		except Exception as e:
			log.error(f"Error al capturar ventana activa: {e}", exc_info=True)
			return None
	
	def captureRegion(self, x1, y1, x2, y2):
		"""
		Captura una región específica de la pantalla
		
		Args:
			x1 (int): Coordenada X superior izquierda
			y1 (int): Coordenada Y superior izquierda
			x2 (int): Coordenada X inferior derecha
			y2 (int): Coordenada Y inferior derecha
		
		Returns:
			str: Imagen en formato base64, o None si falla
		"""
		if not PIL_AVAILABLE:
			return None
		
		try:
			# Capturar región
			bbox = (x1, y1, x2, y2)
			screenshot = ImageGrab.grab(bbox=bbox)
			
			return self._imageToBase64(screenshot)
			
		except Exception as e:
			log.error(f"Error al capturar región: {e}", exc_info=True)
			return None
	
	def _imageToBase64(self, image, format="PNG", quality=85):
		"""
		Convierte una imagen PIL a base64
		
		Args:
			image: Objeto Image de PIL
			format (str): Formato de salida (PNG, JPEG, etc.)
			quality (int): Calidad para JPEG (1-100)
		
		Returns:
			str: Imagen codificada en base64
		"""
		try:
			# Optimizar tamaño si es muy grande
			max_size = 2048
			if image.width > max_size or image.height > max_size:
				image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
			
			# Convertir a bytes
			buffered = BytesIO()
			
			if format.upper() == "JPEG":
				# Convertir a RGB si tiene canal alpha
				if image.mode == "RGBA":
					image = image.convert("RGB")
				image.save(buffered, format=format, quality=quality, optimize=True)
			else:
				image.save(buffered, format=format, optimize=True)
			
			# Codificar en base64
			img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
			
			return img_base64
			
		except Exception as e:
			log.error(f"Error al convertir imagen a base64: {e}", exc_info=True)
			return None
	
	def captureFromClipboard(self):
		"""
		Captura imagen desde el portapapeles
		
		Returns:
			str: Imagen en formato base64, o None si no hay imagen
		"""
		if not PIL_AVAILABLE:
			return None
		
		try:
			from PIL import ImageGrab
			
			# Intentar obtener imagen del portapapeles
			clipboard_image = ImageGrab.grabclipboard()
			
			if clipboard_image is None:
				log.info("No hay imagen en el portapapeles")
				return None
			
			if not isinstance(clipboard_image, Image.Image):
				log.warning("El contenido del portapapeles no es una imagen")
				return None
			
			return self._imageToBase64(clipboard_image)
			
		except Exception as e:
			log.error(f"Error al capturar desde portapapeles: {e}", exc_info=True)
			return None
