# -*- coding: UTF-8 -*-
"""
Paquete de clientes API para servicios de IA
"""

from .openai_client import OpenAIClient
from .gemini_client import GeminiClient

__all__ = ['OpenAIClient', 'GeminiClient']

