# -*- coding: UTF-8 -*-
"""
Diálogo para mostrar resultados de descripción de imágenes
"""

import wx
import gui
import re


def markdown_to_html(markdown_text):
	"""
	Convierte Markdown simple a HTML
	
	Args:
		markdown_text (str): Texto en formato Markdown
	
	Returns:
		str: HTML generado
	"""
	html = markdown_text
	
	# Escapar HTML existente
	html = html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
	
	# Encabezados
	html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
	html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
	html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
	
	# Negritas y cursivas
	html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
	html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
	html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
	html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)
	html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)
	
	# Listas con viñetas
	html = re.sub(r'^\* (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
	html = re.sub(r'^\- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
	html = re.sub(r'(<li>.*</li>\n?)+', r'<ul>\g<0></ul>', html, flags=re.MULTILINE)
	
	# Listas numeradas
	html = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
	
	# Código en línea
	html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
	
	# Enlaces
	html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
	
	# Párrafos (líneas separadas por doble salto)
	paragraphs = html.split('\n\n')
	html = ''.join(f'<p>{p.replace(chr(10), "<br>")}</p>' for p in paragraphs if p.strip())
	
	# Estilo CSS
	css = """
	<style>
		body { 
			font-family: Arial, sans-serif; 
			line-height: 1.6; 
			padding: 15px;
			color: #333;
		}
		h1, h2, h3 { color: #2c3e50; margin-top: 1em; }
		h1 { font-size: 1.8em; }
		h2 { font-size: 1.5em; }
		h3 { font-size: 1.2em; }
		ul, ol { margin-left: 20px; }
		li { margin: 5px 0; }
		code { 
			background-color: #f4f4f4; 
			padding: 2px 5px; 
			border-radius: 3px;
			font-family: monospace;
		}
		strong { font-weight: bold; }
		em { font-style: italic; }
		a { color: #3498db; text-decoration: none; }
		a:hover { text-decoration: underline; }
		.ai-info {
			margin-top: 20px;
			padding: 10px;
			background-color: #f0f0f0;
			border-left: 4px solid #3498db;
			font-size: 0.9em;
			color: #666;
		}
	</style>
	"""
	
	return f"<!DOCTYPE html><html><head>{css}</head><body>{html}</body></html>"


class ResultDialog(wx.Dialog):
	"""Diálogo para mostrar la descripción de una imagen"""
	
	def __init__(self, parent, title, description, aiProvider=""):
		"""
		Args:
			parent: Ventana padre
			title (str): Título del diálogo
			description (str): Texto de la descripción en Markdown
			aiProvider (str): Nombre del proveedor de IA usado
		"""
		super().__init__(parent, title=title, size=(700, 500))
		
		# Agregar información del proveedor de IA al final
		if aiProvider:
			providerNames = {
				"openai": "OpenAI GPT-4 Vision",
				"gemini": "Google Gemini"
			}
			providerName = providerNames.get(aiProvider, aiProvider)
			description += f'\n\n---\nReconocimiento realizado con: {providerName}'
		
		self.plainText = description  # Guardar texto plano para copiar
		
		panel = wx.Panel(self)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		
		# Usar siempre TextCtrl para evitar problemas con wx.html2
		self.textCtrl = wx.TextCtrl(
			panel,
			value=self.plainText,
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP | wx.TE_RICH2
		)
		# Configurar fuente para mejor legibilidad
		font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
		self.textCtrl.SetFont(font)
		self.textCtrl.SetFocus()
		mainSizer.Add(self.textCtrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
		
		# Botones
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		# Botón Copiar
		copyButton = wx.Button(panel, label="&Copiar al portapapeles")
		copyButton.Bind(wx.EVT_BUTTON, self.onCopy)
		buttonSizer.Add(copyButton, flag=wx.ALL, border=5)
		
		# Botón Cerrar
		closeButton = wx.Button(panel, wx.ID_CLOSE, label="&Cerrar")
		closeButton.SetDefault()
		closeButton.Bind(wx.EVT_BUTTON, self.onClose)
		buttonSizer.Add(closeButton, flag=wx.ALL, border=5)
		
		mainSizer.Add(buttonSizer, flag=wx.ALIGN_CENTER | wx.ALL, border=5)
		
		panel.SetSizer(mainSizer)
		self.CenterOnScreen()
	
	def onCopy(self, event):
		"""Copia el texto al portapapeles"""
		if wx.TheClipboard.Open():
			# Copiar el texto plano sin formato HTML
			wx.TheClipboard.SetData(wx.TextDataObject(self.plainText))
			wx.TheClipboard.Close()
			wx.Bell()
	
	def onClose(self, event):
		"""Cierra el diálogo"""
		self.EndModal(wx.ID_CLOSE)


class WelcomeDialog(wx.Dialog):
	"""Diálogo de bienvenida y ayuda rápida"""
	
	def __init__(self, parent, showDontShowAgain=True):
		"""
		Args:
			parent: Ventana padre
			showDontShowAgain (bool): Si True, muestra el checkbox "No volver a mostrar"
		"""
		super().__init__(parent, title="Ayuda - AI Image Describer", size=(600, 450))
		
		panel = wx.Panel(self)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		
		# Texto de ayuda
		helpText = """¡Bienvenido a AI Image Describer!

Este complemento te permite describir imágenes usando inteligencia artificial.

ATAJOS DE TECLADO:

• NVDA+Control+I: Describe la imagen en el objeto con foco
  - Pulsa una vez: verbaliza la descripción
  - Pulsa dos veces: abre ventana con la descripción

• NVDA+Alt+F: Captura y describe la pantalla completa
  - Pulsa una vez: verbaliza la descripción
  - Pulsa dos veces: abre ventana con la descripción

• NVDA+Alt+C: Describe una imagen desde el portapapeles

• NVDA+Alt+Y: Describe una imagen desde archivo

• NVDA+Alt+H: Muestra esta ayuda

CONFIGURACIÓN:

Ve a Preferencias de NVDA > Opciones > AI Image Describer para:
• Configurar tu API key de OpenAI o Google Gemini
• Ajustar el nivel de detalle y el idioma
• Personalizar otras opciones

PROVEEDORES DISPONIBLES:

• OpenAI (GPT-4 Vision): Requiere API key de pago (muy preciso)
• Google Gemini: Requiere API key (nivel gratuito disponible)

NOTA: Necesitas configurar al menos una API key para usar el complemento.
Puedes obtener tus claves en:
- OpenAI: https://platform.openai.com/api-keys
- Gemini: https://aistudio.google.com/apikey
"""
		
		# TextCtrl básico sin dependencias de html2
		textCtrl = wx.TextCtrl(
			panel,
			value=helpText,
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP | wx.TE_RICH2
		)
		# Configurar fuente monoespaciada para mejor legibilidad
		font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
		textCtrl.SetFont(font)
		textCtrl.SetFocus()
		mainSizer.Add(textCtrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
		
		# Checkbox para no volver a mostrar (solo en primer uso)
		self.dontShowAgain = None
		if showDontShowAgain:
			self.dontShowAgain = wx.CheckBox(panel, label="&No volver a mostrar este mensaje")
			mainSizer.Add(self.dontShowAgain, flag=wx.ALL, border=10)
		
		# Botón OK
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		okButton = wx.Button(panel, wx.ID_OK, label="&Entendido")
		okButton.SetDefault()
		okButton.Bind(wx.EVT_BUTTON, self.onOK)
		buttonSizer.Add(okButton, flag=wx.ALL, border=5)
		
		mainSizer.Add(buttonSizer, flag=wx.ALIGN_CENTER | wx.ALL, border=5)
		
		panel.SetSizer(mainSizer)
		self.CenterOnScreen()
	
	def onOK(self, event):
		"""Cierra el diálogo"""
		self.EndModal(wx.ID_OK)
	
	def shouldNotShowAgain(self):
		"""Retorna True si el usuario marcó la opción de no volver a mostrar"""
		if self.dontShowAgain:
			return self.dontShowAgain.GetValue()
		return False
