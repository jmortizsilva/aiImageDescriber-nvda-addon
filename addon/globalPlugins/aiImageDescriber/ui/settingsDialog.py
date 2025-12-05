# -*- coding: UTF-8 -*-
"""
Panel de configuración para AI Image Describer
"""

import wx
import config
import gui
from gui import guiHelper, nvdaControls
from gui.settingsDialogs import SettingsPanel
from logHandler import log


class AIImageDescriberSettingsPanel(SettingsPanel):
	"""Panel de configuración en las preferencias de NVDA"""
	
	# Translators: Título del panel de configuración
	title = "AI Image Describer"
	
	def makeSettings(self, settingsSizer):
		"""Crea los controles de configuración"""
		
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		
		# Proveedor de IA
		# Translators: Etiqueta para seleccionar proveedor
		providerLabel = _("&Proveedor de IA:")
		providerChoices = ["OpenAI GPT-4 Vision", "Google Gemini"]
		self.providerList = sHelper.addLabeledControl(
			providerLabel,
			wx.Choice,
			choices=providerChoices
		)
		
		currentProvider = config.conf["aiImageDescriber"]["apiProvider"]
		providerMap = {"openai": 0, "gemini": 1}
		self.providerList.SetSelection(providerMap.get(currentProvider, 0))
		
		self.providerList.Bind(wx.EVT_CHOICE, self.onProviderChange)
		
		# API Keys
		sHelper.addItem(
			wx.StaticText(self, label="Configuración de API Keys:")
		)
		
		# OpenAI API Key
		# Translators: Etiqueta para API key de OpenAI
		openaiKeyLabel = _("&OpenAI API Key:")
		self.openaiKeyText = sHelper.addLabeledControl(
			openaiKeyLabel,
			wx.TextCtrl,
			value=config.conf["aiImageDescriber"]["openaiApiKey"]
		)
		self.openaiKeyText.SetHint("sk-...")
		
		# Gemini API Key
		# Translators: Etiqueta para API key de Gemini
		geminiKeyLabel = _("&Gemini API Key:")
		self.geminiKeyText = sHelper.addLabeledControl(
			geminiKeyLabel,
			wx.TextCtrl,
			value=config.conf["aiImageDescriber"]["geminiApiKey"]
		)
		self.geminiKeyText.SetHint("AIza...")
		
		# Botón para probar conexión
		# Translators: Etiqueta del botón para probar API
		self.testButton = wx.Button(self, label=_("&Probar conexión"))
		self.testButton.Bind(wx.EVT_BUTTON, self.onTestConnection)
		sHelper.addItem(self.testButton)
		
		# Nivel de detalle
		# Translators: Etiqueta para nivel de detalle
		detailLabel = _("&Nivel de detalle:")
		detailChoices = [
			_("Bajo (más rápido)"),
			_("Auto (recomendado)"),
			_("Alto (más lento)")
		]
		self.detailList = sHelper.addLabeledControl(
			detailLabel,
			wx.Choice,
			choices=detailChoices
		)
		
		currentDetail = config.conf["aiImageDescriber"]["detailLevel"]
		detailMap = {"low": 0, "auto": 1, "high": 2}
		self.detailList.SetSelection(detailMap.get(currentDetail, 1))
		
		# Idioma de descripción
		# Translators: Etiqueta para idioma
		languageLabel = _("I&dioma de descripción:")
		languageChoices = [
			_("Español"),
			_("Inglés"),
			_("Francés")
		]
		self.languageList = sHelper.addLabeledControl(
			languageLabel,
			wx.Choice,
			choices=languageChoices
		)
		
		currentLanguage = config.conf["aiImageDescriber"]["language"]
		langMap = {"es": 0, "en": 1, "fr": 2}
		self.languageList.SetSelection(langMap.get(currentLanguage, 0))
		
		# Anunciar procesamiento
		# Translators: Etiqueta para checkbox de anuncio
		self.announceCheckbox = wx.CheckBox(
			self,
			label=_("&Anunciar cuando se está procesando una imagen")
		)
		self.announceCheckbox.SetValue(
			config.conf["aiImageDescriber"]["announceProcessing"]
		)
		sHelper.addItem(self.announceCheckbox)
		
		# Información de atajos
		sHelper.addItem(
			wx.StaticText(
				self,
				label="\nAtajos de teclado:\n"
				"NVDA+Control+I: Describir imagen en el foco (doble: ventana)\n"
				"NVDA+Alt+F: Capturar pantalla completa (doble: ventana)\n"
				"NVDA+Alt+C: Describir desde portapapeles\n"
				"NVDA+Alt+Y: Cargar imagen desde archivo\n"
				"NVDA+Alt+H: Mostrar ayuda"
			)
		)
	
	def onProviderChange(self, event):
		"""Maneja el cambio de proveedor"""
		pass
	
	def onTestConnection(self, event):
		"""Prueba la conexión con la API seleccionada"""
		provider = self.providerList.GetSelection()
		
		try:
			if provider == 0:  # OpenAI
				apiKey = self.openaiKeyText.GetValue()
				if not apiKey:
					gui.messageBox(
						_("Por favor, ingresa tu API key de OpenAI"),
						_("Error"),
						wx.OK | wx.ICON_ERROR
					)
					return
				
				from ..apiClients.openai_client import OpenAIClient
				client = OpenAIClient(apiKey)
				
				if client.testConnection():
					gui.messageBox(
						_("Conexión exitosa con OpenAI"),
						_("Éxito"),
						wx.OK | wx.ICON_INFORMATION
					)
				else:
					gui.messageBox(
						_("No se pudo conectar con OpenAI. Verifica tu API key."),
						_("Error"),
						wx.OK | wx.ICON_ERROR
					)
			
			elif provider == 1:  # Gemini
				apiKey = self.geminiKeyText.GetValue()
				if not apiKey:
					gui.messageBox(
						_("Por favor, ingresa tu API key de Gemini"),
						_("Error"),
						wx.OK | wx.ICON_ERROR
					)
					return
				
				from ..apiClients.gemini_client import GeminiClient
				client = GeminiClient(apiKey)
				
				if client.testConnection():
					gui.messageBox(
						_("Conexión exitosa con Gemini"),
						_("Éxito"),
						wx.OK | wx.ICON_INFORMATION
					)
				else:
					gui.messageBox(
						_("No se pudo conectar con Gemini. Verifica tu API key."),
						_("Error"),
						wx.OK | wx.ICON_ERROR
					)
		
		except Exception as e:
			log.error(f"Error al probar conexión: {e}", exc_info=True)
			gui.messageBox(
				_("Error al probar conexión: {error}").format(error=str(e)),
				_("Error"),
				wx.OK | wx.ICON_ERROR
			)
	
	def onSave(self):
		"""Guarda la configuración"""
		# Proveedor
		providerIndex = self.providerList.GetSelection()
		providerMap = {0: "openai", 1: "gemini"}
		config.conf["aiImageDescriber"]["apiProvider"] = providerMap.get(providerIndex, "openai")
		
		# API Keys
		config.conf["aiImageDescriber"]["openaiApiKey"] = self.openaiKeyText.GetValue()
		config.conf["aiImageDescriber"]["geminiApiKey"] = self.geminiKeyText.GetValue()
		
		# Nivel de detalle
		detailIndex = self.detailList.GetSelection()
		detailMap = {0: "low", 1: "auto", 2: "high"}
		config.conf["aiImageDescriber"]["detailLevel"] = detailMap.get(detailIndex, "auto")
		
		# Idioma
		langIndex = self.languageList.GetSelection()
		langMap = {0: "es", 1: "en", 2: "fr"}
		config.conf["aiImageDescriber"]["language"] = langMap.get(langIndex, "es")
		
		# Anunciar procesamiento
		config.conf["aiImageDescriber"]["announceProcessing"] = self.announceCheckbox.GetValue()
		
		# Recargar el cliente API con la nueva configuración
		try:
			# Importar la referencia global al plugin
			from .. import _globalPluginInstance
			if _globalPluginInstance:
				_globalPluginInstance._loadAPIClient()
				log.info("Cliente API recargado después de guardar configuración")
		except Exception as e:
			log.error(f"Error al recargar cliente API: {e}", exc_info=True)


# Función auxiliar para traducción (placeholder)
def _(text):
	"""Función de traducción placeholder"""
	return text
