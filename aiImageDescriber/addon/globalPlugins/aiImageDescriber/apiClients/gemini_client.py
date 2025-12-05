# -*- coding: UTF-8 -*-
"""
Cliente para Google Gemini API
Basado en la documentación oficial: https://ai.google.dev/gemini-api/docs/vision
"""

import json
from logHandler import log

try:
	import requests
	REQUESTS_AVAILABLE = True
except ImportError:
	log.warning("requests no disponible")
	REQUESTS_AVAILABLE = False


class GeminiClient:
	"""Cliente para interactuar con Google Gemini"""
	
	# URL correcta según documentación oficial
	API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
	DEFAULT_MODEL = "gemini-1.5-flash-latest"  # Modelo con soporte para visión
	FALLBACK_MODELS = ["gemini-1.5-flash", "gemini-1.5-pro-latest", "gemini-pro-vision"]
	
	def __init__(self, apiKey):
		"""
		Inicializa el cliente de Gemini
		
		Args:
			apiKey (str): Clave API de Google Gemini
		"""
		self.apiKey = apiKey
		self.model = self.DEFAULT_MODEL
		self._modelDetected = False  # Flag para saber si ya detectamos el modelo
	
	def describeImage(self, imageBase64, detail="auto", language="es", maxTokens=2048):
		"""
		Describe una imagen usando Gemini
		
		Args:
			imageBase64 (str): Imagen codificada en base64
			detail (str): Nivel de detalle (no usado en Gemini)
			language (str): Idioma de respuesta
			maxTokens (int): Máximo de tokens en la respuesta
		
		Returns:
			str: Descripción de la imagen
		"""
		if not REQUESTS_AVAILABLE:
			raise Exception("requests no está instalado. Instala con: pip install requests")
		
		# Detectar modelo disponible si no se ha hecho antes
		if not self._modelDetected:
			log.info("Detectando modelo de Gemini disponible...")
			if not self._detectAvailableModel():
				raise Exception(
					"No se pudo encontrar un modelo de Gemini compatible. "
					"Verifica que tu API key tenga acceso a Generative AI API en https://aistudio.google.com/apikey"
				)
			self._modelDetected = True
			log.info(f"Usando modelo de Gemini: {self.model}")
		
		try:
			# Preparar prompt según nivel de detalle e idioma
			if detail == "low":
				# Descripción breve y concisa (ahorra tokens)
				prompts = {
					"es": "Describe brevemente esta imagen en 1-2 frases: qué es y qué está pasando.",
					"en": "Briefly describe this image in 1-2 sentences: what it is and what's happening.",
					"fr": "Décris brièvement cette image en 1-2 phrases: ce que c'est et ce qui se passe."
				}
				maxTokensToUse = 150
			elif detail == "high":
				# Descripción muy detallada (usa más tokens)
				prompts = {
					"es": (
						"Describe esta imagen de forma muy detallada y estructurada para una persona con discapacidad visual. "
						"Incluye:\n"
						"1. Escena general y contexto detallado\n"
						"2. Objetos principales y secundarios con su disposición espacial exacta\n"
						"3. Personas presentes: número, posición, edad aproximada, acciones, expresiones, ropa y accesorios\n"
						"4. Colores específicos, iluminación, sombras y texturas\n"
						"5. Texto visible: transcribe todo el texto legible\n"
						"6. Ambiente, emociones y atmósfera que transmite\n"
						"7. Detalles de fondo y elementos menos prominentes\n"
						"Sé exhaustivo, específico y meticuloso."
					),
					"en": (
						"Describe this image in great detail and structured way for a visually impaired person. "
						"Include:\n"
						"1. General scene and detailed context\n"
						"2. Main and secondary objects with exact spatial arrangement\n"
						"3. People present: number, position, approximate age, actions, expressions, clothing and accessories\n"
						"4. Specific colors, lighting, shadows and textures\n"
						"5. Visible text: transcribe all readable text\n"
						"6. Mood, emotions and atmosphere conveyed\n"
						"7. Background details and less prominent elements\n"
						"Be exhaustive, specific and meticulous."
					),
					"fr": (
						"Décris cette image de manière très détaillée et structurée pour une personne malvoyante. "
						"Inclure:\n"
						"1. Scène générale et contexte détaillé\n"
						"2. Objets principaux et secondaires avec disposition spatiale exacte\n"
						"3. Personnes présentes: nombre, position, âge approximatif, actions, expressions, vêtements et accessoires\n"
						"4. Couleurs spécifiques, éclairage, ombres et textures\n"
						"5. Texte visible: transcrire tout le texte lisible\n"
						"6. Ambiance, émotions et atmosphère transmises\n"
						"7. Détails d'arrière-plan et éléments moins proéminents\n"
						"Sois exhaustif, spécifique et méticuleux."
					)
				}
				maxTokensToUse = maxTokens
			else:  # auto o cualquier otro valor = descripción balanceada
				# Descripción equilibrada (balance entre detalle y tokens)
				prompts = {
					"es": (
						"Describe esta imagen de forma clara para una persona con discapacidad visual. "
						"Incluye: escena general, objetos principales, personas (si las hay), colores relevantes, "
						"texto visible, y el mensaje o propósito de la imagen. Sé específico pero conciso."
					),
					"en": (
						"Describe this image clearly for a visually impaired person. "
						"Include: general scene, main objects, people (if any), relevant colors, "
						"visible text, and the message or purpose of the image. Be specific but concise."
					),
					"fr": (
						"Décris cette image clairement pour une personne malvoyante. "
						"Inclure: scène générale, objets principaux, personnes (le cas échéant), couleurs pertinentes, "
						"texte visible, et le message ou l'objectif de l'image. Sois précis mais concis."
					)
				}
				maxTokensToUse = 500  # Reducido de 800 a 500 para nivel AUTO
			
			prompt = prompts.get(language, prompts["es"])
			
			# URL con API key como query parameter
			url = self.API_URL.format(model=self.model) + f"?key={self.apiKey}"
			
			# Preparar headers
			headers = {
				"Content-Type": "application/json"
			}
			
			# Preparar payload según formato REST de Gemini
			payload = {
				"contents": [{
					"parts": [
						{"text": prompt},
						{
							"inline_data": {
								"mime_type": "image/png",
								"data": imageBase64
							}
						}
					]
				}],
				"generationConfig": {
					"maxOutputTokens": maxTokensToUse,
					"temperature": 0.4
				}
			}
			
			# Hacer petición
			log.info("Enviando petición a Google Gemini...")
			log.debug(f"URL: {self.API_URL.format(model=self.model)}")
			
			response = requests.post(
				url,
				headers=headers,
				json=payload,
				timeout=30
			)
			
			log.info(f"Respuesta Gemini - Status: {response.status_code}")
			
			# Verificar respuesta
			if response.status_code != 200:
				log.error(f"Error de Gemini. Respuesta: {response.text[:500]}")
				response.raise_for_status()
			
			# Extraer descripción
			result = response.json()
			log.info(f"Respuesta completa de Gemini: {json.dumps(result, indent=2)[:2000]}")
			
			if "candidates" not in result or len(result["candidates"]) == 0:
				log.error(f"Estructura de respuesta: {list(result.keys())}")
				raise Exception("No se recibió respuesta de Gemini")
			
			candidate = result["candidates"][0]
			log.info(f"Candidate completo: {json.dumps(candidate, indent=2)[:1000]}")
			
			# Verificar si hay filtros de seguridad
			if "finishReason" in candidate:
				finish_reason = candidate["finishReason"]
				log.info(f"Finish reason: {finish_reason}")
				if finish_reason == "SAFETY":
					raise Exception("La respuesta fue bloqueada por filtros de seguridad de Gemini")
				elif finish_reason == "RECITATION":
					raise Exception("La respuesta fue bloqueada por detección de recitación")
				elif finish_reason == "MAX_TOKENS":
					# En Gemini 2.5, los thinking tokens pueden consumir todo el límite
					# Si no hay contenido, es un error
					if "content" not in candidate or "parts" not in candidate.get("content", {}):
						raise Exception(
							"El modelo alcanzó el límite de tokens antes de generar respuesta. "
							"Esto puede deberse a 'thinking tokens' internos del modelo. "
							"El límite se aumentó automáticamente, intenta de nuevo."
						)
			
			if "content" not in candidate:
				log.error(f"Candidate structure: {json.dumps(candidate, indent=2)[:500]}")
				raise Exception("Respuesta de Gemini sin campo 'content'")
			
			content = candidate["content"]
			if "parts" not in content:
				log.error(f"Content structure: {json.dumps(content, indent=2)[:500]}")
				raise Exception("Respuesta de Gemini sin campo 'parts'")
			
			parts = content["parts"]
			if not parts or len(parts) == 0:
				raise Exception("Respuesta de Gemini vacía")
			
			description = parts[0].get("text", "")
			if not description:
				log.error(f"Part structure: {json.dumps(parts[0], indent=2)[:500]}")
				raise Exception("No se encontró texto en la respuesta")
			
			log.info("Descripción recibida de Gemini")
			return description.strip()
			
		except requests.exceptions.HTTPError as e:
			error_msg = ""
			try:
				error_data = e.response.json()
				error_msg = error_data.get("error", {}).get("message", "")
			except:
				error_msg = e.response.text[:200]
			
			if e.response.status_code == 400:
				if "API_KEY_INVALID" in error_msg or "API key not valid" in error_msg:
					raise Exception("API key de Gemini inválida o no tiene permisos para Generative AI API")
				else:
					raise Exception(f"Error en la petición: {error_msg}")
			elif e.response.status_code == 404:
				raise Exception(
					f"Modelo '{self.model}' no encontrado. "
					"Verifica que tu API key tenga acceso a Generative AI API "
					"y que esté habilitada en https://aistudio.google.com/apikey"
				)
			elif e.response.status_code == 429:
				raise Exception("Límite de solicitudes excedido. Intenta más tarde")
			elif e.response.status_code == 403:
				raise Exception("API key sin permisos. Habilita Generative AI API en Google AI Studio")
			else:
				raise Exception(f"Error HTTP {e.response.status_code}: {error_msg}")
		
		except requests.exceptions.Timeout:
			raise Exception("Tiempo de espera agotado al conectar con Gemini")
		
		except requests.exceptions.RequestException as e:
			log.error(f"Error en GeminiClient: {e}", exc_info=True)
			raise Exception(f"Error de conexión con Gemini: {str(e)}")
		
		except Exception as e:
			if "API key" in str(e) or "permisos" in str(e):
				raise  # Re-lanzar errores de API key tal cual
			log.error(f"Error inesperado en GeminiClient: {e}", exc_info=True)
			raise Exception(f"Error al procesar respuesta de Gemini: {str(e)}")
	
	def _detectAvailableModel(self):
		"""
		Detecta qué modelo de Gemini está disponible y lo configura
		
		Returns:
			bool: True si encontró un modelo compatible, False en caso contrario
		"""
		if not REQUESTS_AVAILABLE:
			return False
		
		try:
			# URL para listar modelos disponibles
			url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.apiKey}"
			
			response = requests.get(url, timeout=10)
			
			if response.status_code != 200:
				log.error(f"Error al listar modelos de Gemini. Status: {response.status_code}, Response: {response.text[:200]}")
				return False
			
			result = response.json()
			models = result.get("models", [])
			
			if not models:
				log.error("No se encontraron modelos disponibles en Gemini")
				return False
			
			# Extraer nombres de modelos disponibles con soporte para vision
			available_models = []
			for m in models:
				supported_methods = m.get("supportedGenerationMethods", [])
				if "generateContent" in supported_methods:
					name = m.get("name", "")
					# El nombre viene como "models/gemini-1.5-flash", extraer solo el nombre
					if "/" in name:
						name = name.split("/")[-1]
					available_models.append(name)
					log.info(f"Modelo disponible con vision: {name}")
			
			if not available_models:
				log.error("No se encontraron modelos con soporte para vision")
				return False
			
			log.info(f"Modelos disponibles: {', '.join(available_models)}")
			
			# Intentar encontrar un modelo compatible
			# Primero intentar con el modelo por defecto
			if self.DEFAULT_MODEL in available_models:
				log.info(f"Usando modelo por defecto: {self.DEFAULT_MODEL}")
				self.model = self.DEFAULT_MODEL
				return True
			
			# Intentar con modelos fallback
			for fallback in self.FALLBACK_MODELS:
				if fallback in available_models:
					log.info(f"Usando modelo fallback: {fallback}")
					self.model = fallback
					return True
			
			# Usar el primer modelo disponible
			self.model = available_models[0]
			log.info(f"Usando primer modelo disponible: {self.model}")
			return True
				
		except Exception as e:
			log.error(f"Error al detectar modelos de Gemini: {e}", exc_info=True)
			return False
	
	def testConnection(self):
		"""
		Prueba la conexión con la API de Gemini y detecta el modelo disponible
		
		Returns:
			bool: True si la conexión es exitosa, False en caso contrario
		"""
		result = self._detectAvailableModel()
		if result:
			self._modelDetected = True
		return result

