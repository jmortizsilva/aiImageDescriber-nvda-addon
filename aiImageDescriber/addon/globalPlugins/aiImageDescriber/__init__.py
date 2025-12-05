# -*- coding: UTF-8 -*-
"""
AI Image Describer - Global Plugin para NVDA
Describe imágenes usando APIs de IA (OpenAI, Gemini, Be My Eyes)
Autor: jmortizsilva
"""

import globalPluginHandler
import scriptHandler
import api
import config
import gui
import wx
import os
import sys
import subprocess
import threading
from logHandler import log

# Importar ui de NVDA ANTES que nuestros módulos
import ui as nvdaUI

# Variable para controlar si ya se verificaron dependencias
_dependenciesChecked = False
_dependenciesOK = False

def checkAndInstallDependencies():
	"""Verifica e instala dependencias automáticamente si faltan"""
	global _dependenciesChecked, _dependenciesOK
	
	if _dependenciesChecked:
		return _dependenciesOK
	
	_dependenciesChecked = True
	missingDeps = []
	
	# Verificar Pillow (necesario para captura de imágenes)
	try:
		import PIL
		log.info("Pillow disponible")
	except ImportError:
		missingDeps.append("Pillow")
	
	# Verificar requests (necesario para APIs)
	# Nota: requests NO viene por defecto con NVDA, debemos instalarlo
	try:
		import requests
		log.info("requests disponible")
	except ImportError:
		missingDeps.append("requests")
	
	if not missingDeps:
		_dependenciesOK = True
		return True
	
	# Mostrar mensaje informativo sobre dependencias faltantes
	message = (
		"AI Image Describer necesita instalar los siguientes componentes:\n\n"
		+ "\n".join(f"â€¢ {dep}" for dep in missingDeps) + "\n\n"
		"Estos son necesarios para:\n"
		"â€¢ Pillow: Capturar y procesar imágenes\n"
		"â€¢ requests: Comunicarse con las APIs de IA\n\n"
		"Â¿Deseas instalarlos automáticamente?\n"
		"(Se descargará desde Internet, puede tardar 10-30 segundos)"
	)
	
	result = gui.messageBox(
		message,
		"AI Image Describer - Instalación de componentes",
		wx.YES_NO | wx.ICON_QUESTION
	)
	
	if result == wx.YES:
		try:
			nvdaUI.message("Descargando e instalando componentes, por favor espera...")
			
			# Usar el Python de NVDA
			pythonExe = sys.executable
			
			# Instalar cada dependencia
			for dep in missingDeps:
				log.info(f"Instalando {dep}...")
				try:
					subprocess.check_call(
						[pythonExe, "-m", "pip", "install", "--quiet", "--no-warn-script-location", dep],
						stdout=subprocess.DEVNULL,
						stderr=subprocess.DEVNULL,
						timeout=120  # 2 minutos máximo
					)
					log.info(f"{dep} instalado correctamente")
				except subprocess.TimeoutExpired:
					log.error(f"Timeout al instalar {dep}")
					raise Exception(f"La instalación de {dep} tardó demasiado")
			
			nvdaUI.message("Â¡Componentes instalados! Reinicia NVDA para usarlos.")
			
			# Mostrar mensaje de éxito
			gui.messageBox(
				"Los componentes se instalaron correctamente.\n\n"
				"Por favor, REINICIA NVDA para que los cambios tengan efecto.\n\n"
				"Después podrás configurar tu API key y usar el complemento.",
				"Instalación exitosa",
				wx.OK | wx.ICON_INFORMATION
			)
			
			_dependenciesOK = True
			return True
			
		except Exception as e:
			log.error(f"Error al instalar dependencias: {e}", exc_info=True)
			gui.messageBox(
				"No se pudieron instalar los componentes automáticamente.\n\n"
				f"Error: {str(e)}\n\n"
				"Solución manual:\n"
				"1. Abre una terminal como administrador\n"
				f"2. Ejecuta: {pythonExe} -m pip install Pillow requests\n"
				"3. Reinicia NVDA",
				"Error de instalación",
				wx.OK | wx.ICON_ERROR
			)
			return False
	else:
		gui.messageBox(
			"Sin estos componentes, AI Image Describer no puede funcionar.\n\n"
			"Puedes instalarlos más tarde ejecutando:\n"
			f"{sys.executable} -m pip install Pillow requests\n\n"
			"O desinstala el complemento si no deseas usarlo.",
			"Instalación cancelada",
			wx.OK | wx.ICON_WARNING
		)
		return False

# Intentar importar los módulos necesarios
ImageCapture = None
ImageProcessor = None
OpenAIClient = None
GeminiClient = None
AIImageDescriberSettingsPanel = None

try:
	from .imageCapture import ImageCapture
	from .imageProcessor import ImageProcessor
	from .apiClients.openai_client import OpenAIClient
	from .apiClients.gemini_client import GeminiClient
	log.info("Importando AIImageDescriberSettingsPanel...")
	from .ui.settingsDialog import AIImageDescriberSettingsPanel
	log.info("AIImageDescriberSettingsPanel importado correctamente")
except ImportError as e:
	log.error(f"Error al importar dependencias: {e}", exc_info=True)
	# Se intentará instalar al inicializar el plugin

# Configuración por defecto
confspec = {
	"apiProvider": "string(default='openai')",
	"openaiApiKey": "string(default='')",
	"geminiApiKey": "string(default='')",
	"detailLevel": "string(default='auto')",
	"language": "string(default='es')",
	"announceProcessing": "boolean(default=True)",
	"firstRun": "boolean(default=True)",
}

config.conf.spec["aiImageDescriber"] = confspec


def stripMarkdown(text):
	"""
	Elimina formato Markdown para verbalización
	
	Args:
		text (str): Texto con formato Markdown
	
	Returns:
		str: Texto limpio sin formato
	"""
	import re
	# Eliminar encabezados
	text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
	# Eliminar negritas y cursivas
	text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)
	text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
	text = re.sub(r'\*(.+?)\*', r'\1', text)
	text = re.sub(r'__(.+?)__', r'\1', text)
	text = re.sub(r'_(.+?)_', r'\1', text)
	# Eliminar código en línea
	text = re.sub(r'`(.+?)`', r'\1', text)
	# Eliminar enlaces pero mantener el texto
	text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
	# Limpiar listas
	text = re.sub(r'^\*\s+', '', text, flags=re.MULTILINE)
	text = re.sub(r'^\-\s+', '', text, flags=re.MULTILINE)
	text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)
	
	return text.strip()


# Variable global para almacenar la instancia del plugin
_globalPluginInstance = None


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	"""Plugin global para descripción de imágenes con IA"""
	
	# Diccionario de gestos/atajos de teclado
	__gestures = {
		# Comandos básicos (verbalizan la descripción)
		"kb:NVDA+alt+i": "describeImageAtFocus",
		"kb:NVDA+alt+s": "captureFullScreen",
		"kb:NVDA+alt+c": "describeFromClipboard",
		"kb:NVDA+alt+f": "loadImageFromFile",
		
		# Comandos con ventana (añadir Shift)
		"kb:NVDA+alt+shift+i": "describeImageAtFocusWindow",
		"kb:NVDA+alt+shift+s": "captureFullScreenWindow",
		"kb:NVDA+alt+shift+c": "describeFromClipboardWindow",
		"kb:NVDA+alt+shift+f": "loadImageFromFileWindow",
		
		# Otros comandos
		"kb:NVDA+alt+o": "openSettings",
		"kb:NVDA+alt+h": "showHelp",
	}
	
	def __init__(self):
		"""Inicializa el plugin global"""
		super(GlobalPlugin, self).__init__()
		
		# Verificar e instalar dependencias en segundo plano
		wx.CallAfter(self._initializePlugin)
	
	def _initializePlugin(self):
		"""Inicialización real después de verificar dependencias"""
		global ImageCapture, ImageProcessor, OpenAIClient, GeminiClient, AIImageDescriberSettingsPanel
		
		# Verificar e instalar dependencias si es necesario
		if not checkAndInstallDependencies():
			log.error("No se pueden cargar las dependencias de AI Image Describer")
			return
		
		# Intentar importar de nuevo si fallaron antes
		if not ImageCapture:
			try:
				from .imageCapture import ImageCapture
				from .imageProcessor import ImageProcessor
				from .apiClients.openai_client import OpenAIClient
				from .apiClients.gemini_client import GeminiClient
				from .ui.settingsDialog import AIImageDescriberSettingsPanel
			except ImportError as e:
				log.error(f"Error al importar módulos después de instalar dependencias: {e}")
				return
		
		# Inicializar componentes
		self.imageCapture = ImageCapture() if ImageCapture else None
		self.imageProcessor = ImageProcessor() if ImageProcessor else None
		self.currentClient = None
		
		# Almacenar instancia global
		global _globalPluginInstance
		_globalPluginInstance = self
		
		# Cargar configuración y cliente de API
		self._loadAPIClient()
		
		# Agregar panel de configuración al menú de NVDA
		if AIImageDescriberSettingsPanel:
			try:
				log.info("Registrando panel de configuración en NVDA...")
				gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(
					AIImageDescriberSettingsPanel
				)
				log.info("Panel de configuración registrado exitosamente")
			except Exception as e:
				log.error(f"Error al agregar panel de configuración: {e}", exc_info=True)
		else:
			log.warning("AIImageDescriberSettingsPanel no está disponible")
		
		# Agregar entrada al menú Herramientas
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.aiImageDescriberHelpItem = self.toolsMenu.Append(
			wx.ID_ANY,
			"Ayuda de AI Image Describer...",
			"Muestra la ayuda rápida de AI Image Describer"
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onHelpMenu, self.aiImageDescriberHelpItem)
		
		# Mostrar ayuda en el primer uso
		if config.conf["aiImageDescriber"]["firstRun"]:
			wx.CallLater(1000, self._showWelcomeDialog, True)
		
		log.info("AI Image Describer inicializado correctamente")
	
	def terminate(self):
		"""Finaliza el plugin y limpia recursos"""
		try:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(
				AIImageDescriberSettingsPanel
			)
		except (ValueError, IndexError):
			pass
		
		# Eliminar entrada del menú Herramientas
		try:
			self.toolsMenu.Remove(self.aiImageDescriberHelpItem)
		except Exception:
			pass
		
		super(GlobalPlugin, self).terminate()
		log.info("AI Image Describer finalizado")
	
	def onHelpMenu(self, event):
		"""Manejador del menú de ayuda"""
		log.info("onHelpMenu ejecutado desde el menú")
		nvdaUI.message("Abriendo ayuda...")
		self._showWelcomeDialog(isFirstRun=False)
	
	def _showWelcomeDialog(self, isFirstRun=False):
		"""
		Muestra el diálogo de ayuda
		
		Args:
			isFirstRun (bool): Si True, muestra el checkbox "No volver a mostrar"
		"""
		try:
			log.info(f"_showWelcomeDialog iniciando con isFirstRun={isFirstRun}")
			from .ui.resultDialog import WelcomeDialog
			log.info("WelcomeDialog importado correctamente")
			
			dlg = WelcomeDialog(gui.mainFrame, showDontShowAgain=isFirstRun)
			log.info("WelcomeDialog creado correctamente")
			
			result = dlg.ShowModal()
			log.info(f"Dialog mostrado, resultado: {result}")
			
			if result == wx.ID_OK:
				if isFirstRun and dlg.shouldNotShowAgain():
					config.conf["aiImageDescriber"]["firstRun"] = False
					log.info("Usuario marcó 'no volver a mostrar'")
			
			dlg.Destroy()
			log.info("Dialog destruido correctamente")
		except Exception as e:
			log.error(f"Error al mostrar diálogo de ayuda: {e}", exc_info=True)
			# Mostrar mensaje al usuario
			nvdaUI.message(f"Error al abrir la ayuda: {str(e)}")
	
	def _showResultDialog(self, title, description):
		"""Muestra el diálogo con el resultado de la descripción"""
		try:
			from .ui.resultDialog import ResultDialog
			# Verbalizar también para accesibilidad inmediata
			nvdaUI.message("Descripción obtenida. Abriendo ventana...")
			# Obtener el proveedor actual
			provider = config.conf["aiImageDescriber"]["apiProvider"]
			dlg = ResultDialog(gui.mainFrame, title, description, provider)
			dlg.ShowModal()
			dlg.Destroy()
		except Exception as e:
			log.error(f"Error al mostrar diálogo de resultado: {e}", exc_info=True)
			# Fallback: mostrar solo con voz
			nvdaUI.message(description)
	
	def _loadAPIClient(self):
		"""Carga el cliente de API según la configuración"""
		# Reiniciar cliente actual
		self.currentClient = None
		
		provider = config.conf["aiImageDescriber"]["apiProvider"]
		log.info(f"Cargando proveedor de IA: {provider}")
		
		if provider == "openai" and OpenAIClient:
			apiKey = config.conf["aiImageDescriber"]["openaiApiKey"]
			if apiKey:
				self.currentClient = OpenAIClient(apiKey)
				log.info("Cliente OpenAI cargado exitosamente")
			else:
				log.warning("OpenAI seleccionado pero no hay API key configurada")
		elif provider == "gemini" and GeminiClient:
			apiKey = config.conf["aiImageDescriber"]["geminiApiKey"]
			if apiKey:
				self.currentClient = GeminiClient(apiKey)
				log.info("Cliente Gemini cargado exitosamente")
			else:
				log.warning("Gemini seleccionado pero no hay API key configurada")
		else:
			log.warning(f"Proveedor de API no reconocido o no disponible: {provider}")
	
	@scriptHandler.script(
		description="Describe la imagen bajo el foco o cursor del navegador de objetos",
		category="AI Image Describer"
	)
	def script_describeImageAtFocus(self, gesture):
		"""Describe la imagen en el objeto actual."""
		log.info("Script describeImageAtFocus ejecutado")
		if not self._checkConfiguration():
			return
		
		# Verbalizar resultado
		showWindow = False
		
		obj = api.getFocusObject()
		
		if config.conf["aiImageDescriber"]["announceProcessing"]:
			nvdaUI.message("Analizando imagen en el foco...")
		
		# Ejecutar en segundo plano para no bloquear NVDA
		threading.Thread(
			target=self._analyzeObject,
			args=(obj, showWindow),
			daemon=True
		).start()
	
	@scriptHandler.script(
		description="Describe la imagen bajo el foco y muestra el resultado en una ventana",
		category="AI Image Describer"
	)
	def script_describeImageAtFocusWindow(self, gesture):
		"""Describe la imagen en el objeto actual y muestra en ventana."""
		log.info("Script describeImageAtFocusWindow ejecutado")
		if not self._checkConfiguration():
			return
		
		# Mostrar en ventana
		showWindow = True
		
		obj = api.getFocusObject()
		
		if config.conf["aiImageDescriber"]["announceProcessing"]:
			nvdaUI.message("Analizando imagen en el foco...")
		
		# Ejecutar en segundo plano para no bloquear NVDA
		threading.Thread(
			target=self._analyzeObject,
			args=(obj, showWindow),
			daemon=True
		).start()
	
	@scriptHandler.script(
		description="Captura y describe la pantalla completa",
		category="AI Image Describer"
	)
	def script_captureFullScreen(self, gesture):
		"""Captura toda la pantalla y la describe."""
		log.info("Script captureFullScreen ejecutado")
		if not self._checkConfiguration():
			return
		
		# Verbalizar resultado
		showWindow = False
		
		if config.conf["aiImageDescriber"]["announceProcessing"]:
			nvdaUI.message("Capturando pantalla completa...")
		
		threading.Thread(
			target=self._captureAndDescribe,
			args=("full", showWindow),
			daemon=True
		).start()
	
	@scriptHandler.script(
		description="Captura y describe la pantalla completa mostrando el resultado en una ventana",
		category="AI Image Describer"
	)
	def script_captureFullScreenWindow(self, gesture):
		"""Captura toda la pantalla, la describe y muestra en ventana."""
		log.info("Script captureFullScreenWindow ejecutado")
		if not self._checkConfiguration():
			return
		
		# Mostrar en ventana
		showWindow = True
		
		if config.conf["aiImageDescriber"]["announceProcessing"]:
			nvdaUI.message("Capturando pantalla completa...")
		
		threading.Thread(
			target=self._captureAndDescribe,
			args=("full", showWindow),
			daemon=True
		).start()
	
	@scriptHandler.script(
		description="Describe una imagen desde el portapapeles",
		category="AI Image Describer"
	)
	def script_describeFromClipboard(self, gesture):
		"""Describe una imagen desde el portapapeles."""
		log.info("Script describeFromClipboard ejecutado")
		if not self._checkConfiguration():
			return
		
		# Verbalizar resultado
		showWindow = False
		
		if config.conf["aiImageDescriber"]["announceProcessing"]:
			nvdaUI.message("Analizando imagen desde el portapapeles...")
		
		# Ejecutar en segundo plano
		threading.Thread(
			target=self._captureAndDescribe,
			args=("clipboard", showWindow),
			daemon=True
		).start()
	
	@scriptHandler.script(
		description="Describe una imagen desde el portapapeles y muestra el resultado en una ventana",
		category="AI Image Describer"
	)
	def script_describeFromClipboardWindow(self, gesture):
		"""Describe una imagen desde el portapapeles y muestra en ventana."""
		log.info("Script describeFromClipboardWindow ejecutado")
		if not self._checkConfiguration():
			return
		
		# Mostrar en ventana
		showWindow = True
		
		if config.conf["aiImageDescriber"]["announceProcessing"]:
			nvdaUI.message("Analizando imagen desde el portapapeles...")
		
		# Ejecutar en segundo plano
		threading.Thread(
			target=self._captureAndDescribe,
			args=("clipboard", showWindow),
			daemon=True
		).start()
	
	@scriptHandler.script(
		description="Abre un diálogo para cargar y describir una imagen desde archivo",
		category="AI Image Describer"
	)
	def script_loadImageFromFile(self, gesture):
		"""Carga una imagen desde un archivo y la describe"""
		if not self._checkConfiguration():
			return
		
		# Verbalizar resultado
		showWindow = False
		
		# Crear diálogo de selección de archivo
		wx.CallAfter(self._showFileDialog, showWindow)
	
	@scriptHandler.script(
		description="Abre un diálogo para cargar una imagen desde archivo y muestra el resultado en una ventana",
		category="AI Image Describer"
	)
	def script_loadImageFromFileWindow(self, gesture):
		"""Carga una imagen desde un archivo y la describe en ventana"""
		if not self._checkConfiguration():
			return
		
		# Mostrar en ventana
		showWindow = True
		
		# Crear diálogo de selección de archivo
		wx.CallAfter(self._showFileDialog, showWindow)
	
	@scriptHandler.script(
		description="Abre la configuración de AI Image Describer",
		category="AI Image Describer"
	)
	def script_openSettings(self, gesture):
		"""Abre el panel de configuración"""
		wx.CallAfter(
			gui.mainFrame._popupSettingsDialog,
			gui.settingsDialogs.NVDASettingsDialog,
			AIImageDescriberSettingsPanel
		)
	
	@scriptHandler.script(
		description="Muestra la ayuda rápida de AI Image Describer",
		category="AI Image Describer"
	)
	def script_showHelp(self, gesture):
		"""Muestra el diálogo de ayuda"""
		log.info("script_showHelp ejecutado por atajo de teclado")
		nvdaUI.message("Abriendo ayuda...")
		# Usar wx.CallLater en lugar de CallAfter para dar tiempo al mensaje
		wx.CallLater(100, self._showWelcomeDialog, False)
	
	def _checkConfiguration(self):
		"""Verifica que el plugin esté configurado correctamente"""
		if not self.currentClient:
			nvdaUI.message("Error: No hay un proveedor de IA configurado. Configura tu API key en las preferencias de NVDA.")
			return False
		
		if not self.imageCapture or not self.imageProcessor:
			nvdaUI.message("Error: Módulos de captura no disponibles")
			return False
		
		return True
	
	def _analyzeObject(self, obj, showWindow=True):
		"""Analiza un objeto NVDA y describe su imagen"""
		try:
			# Extraer imagen del objeto
			imageData = self.imageProcessor.extractFromObject(obj)
			
			if not imageData:
				nvdaUI.message("No se pudo extraer la imagen del objeto")
				return
			
			# Obtener configuración
			detailLevel = config.conf["aiImageDescriber"]["detailLevel"]
			language = config.conf["aiImageDescriber"]["language"]
			log.info(f"_analyzeObject: Usando detailLevel='{detailLevel}', language='{language}', showWindow={showWindow}")
			
			# Obtener descripción de la API
			description = self.currentClient.describeImage(
				imageData,
				detail=detailLevel,
				language=language,
				maxTokens=4000  # Aumentado para Gemini thinking tokens
			)
			
			# Mostrar resultado según preferencia
			if showWindow:
				wx.CallAfter(self._showResultDialog, "Descripción de imagen en foco", description)
			else:
				# Limpiar Markdown para verbalización
				cleanText = stripMarkdown(description)
				nvdaUI.message(cleanText)
			
		except Exception as e:
			log.error(f"Error al analizar objeto: {e}", exc_info=True)
			nvdaUI.message(f"Error al analizar imagen: {str(e)}")
	
	def _captureAndDescribe(self, captureType="full", showWindow=True):
		"""Captura pantalla y la describe"""
		try:
			# Capturar imagen según tipo
			if captureType == "full":
				imageData = self.imageCapture.captureFullScreen()
				title = "Descripción de pantalla completa"
			elif captureType == "clipboard":
				imageData = self.imageCapture.captureFromClipboard()
				title = "Descripción de imagen del portapapeles"
			else:
				nvdaUI.message("Tipo de captura no soportado")
				return
		
			if not imageData:
				if captureType == "clipboard":
					nvdaUI.message("No hay ninguna imagen en el portapapeles")
				else:
					nvdaUI.message("Error al capturar la pantalla")
				return
		
			# Obtener configuración
			detailLevel = config.conf["aiImageDescriber"]["detailLevel"]
			language = config.conf["aiImageDescriber"]["language"]
			log.info(f"_captureAndDescribe: captureType='{captureType}', detailLevel='{detailLevel}', language='{language}', showWindow={showWindow}")
		
			# Describir imagen
			description = self.currentClient.describeImage(
			imageData,
			detail=detailLevel,
			language=language,
			maxTokens=4000  # Aumentado para Gemini thinking tokens
		)
		
			# Mostrar resultado según preferencia
			if showWindow:
				wx.CallAfter(self._showResultDialog, title, description)
			else:
				# Limpiar Markdown para verbalización
				cleanText = stripMarkdown(description)
				nvdaUI.message(cleanText)
		
		except Exception as e:
			log.error(f"Error al capturar y describir: {e}", exc_info=True)
			nvdaUI.message(f"Error: {str(e)}")

	def _showFileDialog(self, showWindow=False):
		"""Muestra diálogo para seleccionar archivo de imagen"""
		try:
			wildcard = "Archivos de imagen|*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.webp|Todos los archivos|*.*"
			
			dlg = wx.FileDialog(
				gui.mainFrame,
				message="Selecciona una imagen para describir",
				wildcard=wildcard,
				style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
			)
			
			if dlg.ShowModal() == wx.ID_OK:
				filePath = dlg.GetPath()
				nvdaUI.message("Analizando imagen desde archivo...")
				
				# Procesar en segundo plano
				threading.Thread(
					target=self._analyzeImageFile,
					args=(filePath, showWindow),
					daemon=True
				).start()
			
			dlg.Destroy()
			
		except Exception as e:
			log.error(f"Error al mostrar diálogo de archivo: {e}", exc_info=True)
			nvdaUI.message(f"Error: {str(e)}")
	
	def _analyzeImageFile(self, filePath, showWindow=False):
		"""Analiza una imagen desde archivo"""
		try:
			# Leer imagen
			imageData = self.imageProcessor.loadFromFile(filePath)
			
			if not imageData:
				nvdaUI.message("No se pudo cargar la imagen")
				return
			
			# Obtener configuración
			detailLevel = config.conf["aiImageDescriber"]["detailLevel"]
			language = config.conf["aiImageDescriber"]["language"]
			log.info(f"_analyzeImageFile: filePath='{filePath}', detailLevel='{detailLevel}', language='{language}', showWindow={showWindow}")
			
			# Describir imagen
			description = self.currentClient.describeImage(
				imageData,
				detail=detailLevel,
				language=language,
				maxTokens=4000  # Aumentado para Gemini thinking tokens
			)
			
			fileName = os.path.basename(filePath)
			
			# Mostrar resultado según preferencia
			if showWindow:
				wx.CallAfter(self._showResultDialog, f"Descripción de {fileName}", description)
			else:
				# Limpiar Markdown para verbalización
				cleanText = stripMarkdown(description)
				nvdaUI.message(f"Descripción de {fileName}: {cleanText}")
			
		except Exception as e:
			log.error(f"Error al analizar archivo: {e}", exc_info=True)
			nvdaUI.message(f"Error: {str(e)}")
