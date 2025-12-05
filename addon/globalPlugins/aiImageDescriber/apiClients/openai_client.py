# -*- coding: UTF-8 -*-
"""
Cliente para OpenAI GPT-4 Vision API
"""

import json
from logHandler import log

try:
	import requests
	REQUESTS_AVAILABLE = True
except ImportError:
	log.warning("requests no disponible")
	REQUESTS_AVAILABLE = False


class OpenAIClient:
	"""Cliente para interactuar con OpenAI GPT-4 Vision"""
	
	API_URL = "https://api.openai.com/v1/chat/completions"
	DEFAULT_MODEL = "gpt-4o"  # Modelo más reciente con visión
	
	def __init__(self, apiKey):
		"""
		Inicializa el cliente de OpenAI
		
		Args:
			apiKey (str): Clave API de OpenAI
		"""
		self.apiKey = apiKey
		self.model = self.DEFAULT_MODEL
	
	def describeImage(self, imageBase64, detail="auto", language="es", maxTokens=500):
		"""
		Describe una imagen usando GPT-4 Vision
		
		Args:
			imageBase64 (str): Imagen codificada en base64
			detail (str): Nivel de detalle - "low", "high", o "auto"
			language (str): Idioma de respuesta
			maxTokens (int): Máximo de tokens en la respuesta
		
		Returns:
			str: Descripción de la imagen
		"""
		if not REQUESTS_AVAILABLE:
			raise Exception("requests no está instalado. Instala con: pip install requests")
		
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
				detailLevel = "low"
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
				detailLevel = "high"
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
				maxTokensToUse = 800
				detailLevel = "auto"
			
			prompt = prompts.get(language, prompts["es"])
			
			# Construir payload
			headers = {
				"Content-Type": "application/json",
				"Authorization": f"Bearer {self.apiKey}"
			}
			
			payload = {
				"model": self.model,
				"messages": [
					{
						"role": "user",
						"content": [
							{
								"type": "text",
								"text": prompt
							},
						{
							"type": "image_url",
							"image_url": {
								"url": f"data:image/png;base64,{imageBase64}",
								"detail": detailLevel
							}
						}
					]
				}
			],
			"max_tokens": maxTokensToUse
		}			# Hacer petición
			log.info("Enviando petición a OpenAI GPT-4 Vision...")
			response = requests.post(
				self.API_URL,
				headers=headers,
				json=payload,
				timeout=30
			)
			
			# Verificar respuesta
			response.raise_for_status()
			
			# Extraer descripción
			result = response.json()
			description = result["choices"][0]["message"]["content"]
			
			log.info("Descripción recibida de OpenAI")
			return description.strip()
			
		except requests.exceptions.HTTPError as e:
			if e.response.status_code == 401:
				raise Exception("API key de OpenAI inválida")
			elif e.response.status_code == 429:
				raise Exception("Límite de solicitudes excedido. Intenta más tarde")
			elif e.response.status_code == 400:
				error_data = e.response.json()
				error_msg = error_data.get("error", {}).get("message", "Error desconocido")
				raise Exception(f"Error en la petición: {error_msg}")
			else:
				raise Exception(f"Error HTTP {e.response.status_code}: {str(e)}")
		
		except requests.exceptions.Timeout:
			raise Exception("Tiempo de espera agotado. Verifica tu conexión")
		
		except requests.exceptions.ConnectionError:
			raise Exception("Error de conexión. Verifica tu conexión a internet")
		
		except Exception as e:
			log.error(f"Error en OpenAI client: {e}", exc_info=True)
			raise Exception(f"Error al procesar imagen: {str(e)}")
	
	def testConnection(self):
		"""
		Prueba la conexión con la API de OpenAI
		
		Returns:
			bool: True si la conexión es exitosa
		"""
		try:
			headers = {
				"Authorization": f"Bearer {self.apiKey}"
			}
			
			response = requests.get(
				"https://api.openai.com/v1/models",
				headers=headers,
				timeout=10
			)
			
			response.raise_for_status()
			return True
			
		except Exception as e:
			log.error(f"Error al probar conexión con OpenAI: {e}")
			return False
