# -*- coding: UTF-8 -*-
"""Build variables for AI Image Describer add-on"""

import os.path

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Since some strings in `addon_info` are translatable,
# we need to include them in the .po files.
# Gettext recognizes only strings given as parameters to the `_` function.
# To avoid initializing translations in this module we simply roll our own "fake" `_` function
# which returns whatever is given to it as an argument.
def _(arg):
	return arg

# Add-on information variables
addon_info = {
	# add-on Name, internal for nvda
	"addon_name": "aiImageDescriber",
	# Add-on summary, usually the user visible name of the addon.
	# Translators: Summary for this add-on
	# to be shown on installation and add-on information found in Add-ons Manager.
	"addon_summary": _("AI Image Describer"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description": _("""Complemento para NVDA que utiliza inteligencia artificial para describir imágenes.
Características:
- Describe imágenes en documentos (Word, navegadores, PDFs)
- Captura y describe regiones de la pantalla
- Carga imágenes desde archivos
- Soporta múltiples proveedores: OpenAI GPT-4 Vision, Google Gemini, Be My Eyes
"""),
	# version
	"addon_version": "0.1.0",
	# Author(s)
	"addon_author": "jmortizsilva",
	# URL for the add-on documentation support
	"addon_url": "https://github.com/jmortizsilva/aiImageDescriber",
	# File name for the add-on help file.
	"addon_docFileName": "readme.html",
	# Minimum NVDA version supported (e.g. "2018.3")
	"addon_minimumNVDAVersion": "2021.1",
	# Last NVDA version supported/tested (e.g. "2018.4", ideally more recent than minimum version)
	"addon_lastTestedNVDAVersion": "2025.3",
	# Add-on update channel (default is None, denoting stable releases,
	# and for development releases, use "dev".)
	# Do not change unless you know what you are doing!
	"addon_updateChannel": None,
	# Add-on license such as GPL 2
	"addon_license": "GPL v2",
	# URL for the license document the ad-on is licensed under
	"addon_licenseURL": "https://www.gnu.org/licenses/gpl-2.0.html",
}

# Define the python files that are the sources of your add-on.
# You can either list them out one by one in the pythonSources entry below,
# or use the globSources function to find all python files in a folder.
# The base directory for globSources is the add-on source folder.
# There are a few things to note:
# If the glob pattern includes both a python package and python modules in the package,
# the package path will be preferred over the module path in the generated add-on manifest.
# globSources will not add python modules from packages that are outside the add-on source folder.
# Use either globSources or list out the files you want one by one.
pythonSources = []

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []

# Base language for the NVDA add-on
# If your add-on is written in a language other than english, modify this variable.
# For example, set baseLanguage to "es" if your add-on is primarily written in spanish.
baseLanguage = "es"

# Markdown extensions for add-on documentation
# Most add-ons do not require additional Markdown extensions.
# If you need to add support for markup such as tables, fill out the below list.
# Extensions string must be of the form "markdown.extensions.extensionName"
# e.g. "markdown.extensions.tables" to add tables.
markdownExtensions = []
