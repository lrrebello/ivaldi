import requests
import re
import os
from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from hebraicofacil import cache  # Importar cache de __init__.py
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

bible_bp = Blueprint('bible', __name__)

# Configurações da API
API_KEY = os.getenv('SCRIPTURE_API_KEY', "4e7f66e15147023701132864385df905")
BASE_URL = "https://api.scripture.api.bible/v1"
BIBLE_ID = "0b262f1ed7f084a6-01"

# Mapeamento de IDs de livros para nomes em português
BOOK_NAMES = {
    "GEN": "Gênesis", "EXO": "Êxodo", "LEV": "Levítico", "NUM": "Números", "DEU": "Deuteronômio",
    "JOS": "Josué", "JDG": "Juízes", "1SA": "1 Samuel", "2SA": "2 Samuel", "1KI": "1 Reis",
    "2KI": "2 Reis", "ISA": "Isaías", "JER": "Jeremias", "EZK": "Ezequiel", "HOS": "Oséias",
    "JOL": "Joel", "AMO": "Amós", "OBA": "Obadias", "JON": "Jonas", "MIC": "Miquéias",
    "NAM": "Naum", "HAB": "Habacuque", "ZEP": "Sofonias", "HAG": "Ageu", "ZEC": "Zacarias",
    "MAL": "Malaquias", "PSA": "Salmos", "PRO": "Provérbios", "JOB": "Jó", "SNG": "Cântico dos Cânticos",
    "RUT": "Rute", "LAM": "Lamentações", "ECC": "Eclesiastes", "EST": "Ester", "DAN": "Daniel",
    "EZR": "Esdras", "NEH": "Neemias", "1CH": "1 Crônicas", "2CH": "2 Crônicas"
}

# Mapeamento de IDs de livros para número de capítulos
CHAPTER_COUNTS = {
    "GEN": 50, "EXO": 40, "LEV": 27, "NUM": 36, "DEU": 34,
    "JOS": 24, "JDG": 21, "1SA": 31, "2SA": 24, "1KI": 22, "2KI": 25, "ISA": 66, "JER": 52, "EZK": 48,
    "HOS": 14, "JOL": 3, "AMO": 9, "OBA": 1, "JON": 4, "MIC": 7, "NAM": 3,
    "HAB": 3, "ZEP": 3, "HAG": 2, "ZEC": 14, "MAL": 4, "PSA": 150, "PRO": 31,
    "JOB": 42, "SNG": 8, "RUT": 4, "LAM": 5, "ECC": 12, "EST": 10, "DAN": 12,
    "EZR": 10, "NEH": 13, "1CH": 29, "2CH": 36,
}

# Mapeamento completo de versículos por capítulo para todos os livros
VERSE_COUNTS = {
    "GEN": {1: 31, 2: 25, 3: 24, 4: 26, 5: 32, 6: 22, 7: 24, 8: 22, 9: 29, 10: 32, 11: 32, 12: 20, 13: 18, 14: 24, 15: 21, 16: 16, 17: 27, 18: 33, 19: 38, 20: 18, 21: 34, 22: 24, 23: 20, 24: 67, 25: 34, 26: 35, 27: 46, 28: 22, 29: 35, 30: 43, 31: 55, 32: 32, 33: 20, 34: 31, 35: 29, 36: 43, 37: 36, 38: 30, 39: 23, 40: 23, 41: 57, 42: 38, 43: 34, 44: 34, 45: 28, 46: 34, 47: 31, 48: 22, 49: 33, 50: 26},
    "EXO": {1: 22, 2: 25, 3: 22, 4: 31, 5: 23, 6: 30, 7: 25, 8: 32, 9: 35, 10: 29, 11: 10, 12: 51, 13: 22, 14: 31, 15: 27, 16: 36, 17: 16, 18: 27, 19: 25, 20: 26, 21: 36, 22: 31, 23: 33, 24: 18, 25: 40, 26: 37, 27: 21, 28: 43, 29: 46, 30: 38, 31: 18, 32: 35, 33: 23, 34: 35, 35: 35, 36: 38, 37: 29, 38: 31, 39: 43, 40: 38},
    "LEV": {1: 17, 2: 16, 3: 17, 4: 35, 5: 19, 6: 30, 7: 38, 8: 36, 9: 24, 10: 20, 11: 47, 12: 8, 13: 59, 14: 57, 15: 33, 16: 34, 17: 16, 18: 30, 19: 37, 20: 27, 21: 24, 22: 33, 23: 44, 24: 23, 25: 55, 26: 46, 27: 34},
    "NUM": {1: 54, 2: 34, 3: 51, 4: 49, 5: 31, 6: 27, 7: 89, 8: 26, 9: 23, 10: 36, 11: 35, 12: 16, 13: 33, 14: 45, 15: 41, 16: 50, 17: 13, 18: 32, 19: 22, 20: 29, 21: 35, 22: 41, 23: 30, 24: 25, 25: 18, 26: 65, 27: 23, 28: 31, 29: 40, 30: 16, 31: 54, 32: 42, 33: 56, 34: 29, 35: 34, 36: 13},
    "DEU": {1: 46, 2: 37, 3: 29, 4: 49, 5: 33, 6: 25, 7: 26, 8: 20, 9: 29, 10: 22, 11: 32, 12: 32, 13: 18, 14: 29, 15: 23, 16: 22, 17: 20, 18: 22, 19: 21, 20: 20, 21: 23, 22: 30, 23: 25, 24: 22, 25: 19, 26: 19, 27: 26, 28: 68, 29: 29, 30: 20, 31: 30, 32: 52, 33: 29, 34: 12},
    "JOS": {1: 18, 2: 24, 3: 17, 4: 24, 5: 15, 6: 27, 7: 26, 8: 35, 9: 27, 10: 43, 11: 23, 12: 24, 13: 33, 14: 15, 15: 63, 16: 10, 17: 18, 18: 28, 19: 51, 20: 9, 21: 45, 22: 34, 23: 16, 24: 33},
    "JDG": {1: 36, 2: 23, 3: 31, 4: 24, 5: 31, 6: 40, 7: 25, 8: 35, 9: 57, 10: 18, 11: 40, 12: 15, 13: 25, 14: 20, 15: 20, 16: 31, 17: 13, 18: 31, 19: 30, 20: 48, 21: 25},
    "1SA": {1: 28, 2: 36, 3: 21, 4: 22, 5: 12, 6: 21, 7: 17, 8: 22, 9: 27, 10: 27, 11: 15, 12: 25, 13: 23, 14: 52, 15: 35, 16: 23, 17: 58, 18: 30, 19: 24, 20: 42, 21: 15, 22: 23, 23: 29, 24: 22, 25: 44, 26: 25, 27: 12, 28: 25, 29: 11, 30: 31, 31: 13},
    "2SA": {1: 27, 2: 32, 3: 39, 4: 12, 5: 25, 6: 23, 7: 29, 8: 18, 9: 13, 10: 19, 11: 27, 12: 31, 13: 39, 14: 33, 15: 37, 16: 23, 17: 29, 18: 33, 19: 43, 20: 26, 21: 22, 22: 51, 23: 39, 24: 25},
    "1KI": {1: 53, 2: 46, 3: 28, 4: 34, 5: 18, 6: 38, 7: 51, 8: 66, 9: 28, 10: 29, 11: 43, 12: 33, 13: 34, 14: 31, 15: 34, 16: 34, 17: 24, 18: 46, 19: 21, 20: 43, 21: 29, 22: 53},
    "2KI": {1: 18, 2: 25, 3: 27, 4: 44, 5: 27, 6: 33, 7: 20, 8: 29, 9: 37, 10: 36, 11: 21, 12: 21, 13: 25, 14: 29, 15: 38, 16: 20, 17: 41, 18: 37, 19: 37, 20: 21, 21: 26, 22: 20, 23: 37, 24: 20, 25: 30},
    "ISA": {1: 31, 2: 22, 3: 26, 4: 6, 5: 30, 6: 13, 7: 25, 8: 22, 9: 21, 10: 34, 11: 16, 12: 6, 13: 22, 14: 32, 15: 9, 16: 14, 17: 14, 18: 7, 19: 25, 20: 6, 21: 17, 22: 25, 23: 18, 24: 23, 25: 12, 26: 21, 27: 13, 28: 29, 29: 24, 30: 33, 31: 9, 32: 20, 33: 24, 34: 17, 35: 10, 36: 22, 37: 38, 38: 22, 39: 8, 40: 31, 41: 29, 42: 25, 43: 28, 44: 28, 45: 25, 46: 13, 47: 15, 48: 22, 49: 26, 50: 11, 51: 23, 52: 15, 53: 12, 54: 17, 55: 13, 56: 12, 57: 21, 58: 14, 59: 21, 60: 22, 61: 11, 62: 12, 63: 19, 64: 12, 65: 25, 66: 24},
    "JER": {1: 19, 2: 37, 3: 25, 4: 31, 5: 31, 6: 30, 7: 34, 8: 22, 9: 26, 10: 25, 11: 23, 12: 17, 13: 27, 14: 22, 15: 21, 16: 21, 17: 27, 18: 23, 19: 15, 20: 18, 21: 14, 22: 30, 23: 40, 24: 10, 25: 38, 26: 24, 27: 22, 28: 17, 29: 32, 30: 24, 31: 40, 32: 44, 33: 26, 34: 22, 35: 19, 36: 32, 37: 21, 38: 28, 39: 18, 40: 16, 41: 18, 42: 22, 43: 13, 44: 30, 45: 5, 46: 28, 47: 7, 48: 47, 49: 39, 50: 46, 51: 64, 52: 34},
    "EZK": {1: 28, 2: 10, 3: 27, 4: 17, 5: 17, 6: 14, 7: 27, 8: 18, 9: 11, 10: 22, 11: 25, 12: 28, 13: 23, 14: 23, 15: 8, 16: 63, 17: 24, 18: 32, 19: 14, 20: 44, 21: 32, 22: 31, 23: 49, 24: 27, 25: 17, 26: 21, 27: 36, 28: 26, 29: 21, 30: 26, 31: 18, 32: 32, 33: 33, 34: 31, 35: 15, 36: 38, 37: 28, 38: 23, 39: 29, 40: 49, 41: 26, 42: 20, 43: 27, 44: 31, 45: 25, 46: 24, 47: 23, 48: 35},
    "HOS": {1: 11, 2: 23, 3: 5, 4: 19, 5: 15, 6: 11, 7: 16, 8: 14, 9: 17, 10: 15, 11: 12, 12: 14, 13: 16, 14: 9},
    "JOL": {1: 20, 2: 32, 3: 21},
    "AMO": {1: 15, 2: 16, 3: 15, 4: 13, 5: 27, 6: 14, 7: 17, 8: 14, 9: 15},
    "OBA": {1: 21},
    "JON": {1: 17, 2: 10, 3: 10, 4: 11},
    "MIC": {1: 16, 2: 13, 3: 12, 4: 14, 5: 15, 6: 16, 7: 20},
    "NAM": {1: 15, 2: 13, 3: 19},
    "HAB": {1: 17, 2: 20, 3: 19},
    "ZEP": {1: 18, 2: 15, 3: 20},
    "HAG": {1: 15, 2: 23},
    "ZEC": {1: 21, 2: 13, 3: 10, 4: 14, 5: 11, 6: 15, 7: 14, 8: 23, 9: 17, 10: 12, 11: 17, 12: 14, 13: 9, 14: 21},
    "MAL": {1: 14, 2: 17, 3: 18, 4: 6},
    "PSA": {1: 6, 2: 12, 3: 8, 4: 8, 5: 12, 6: 10, 7: 17, 8: 9, 9: 20, 10: 18, 11: 7, 12: 8, 13: 6, 14: 7, 15: 5, 16: 11, 17: 15, 18: 50, 19: 14, 20: 9, 21: 13, 22: 31, 23: 6, 24: 10, 25: 22, 26: 12, 27: 14, 28: 9, 29: 11, 30: 12, 31: 24, 32: 11, 33: 22, 34: 22, 35: 28, 36: 12, 37: 40, 38: 22, 39: 13, 40: 17, 41: 13, 42: 11, 43: 5, 44: 26, 45: 17, 46: 11, 47: 9, 48: 14, 49: 20, 50: 23, 51: 19, 52: 9, 53: 6, 54: 7, 55: 23, 56: 13, 57: 11, 58: 11, 59: 17, 60: 12, 61: 8, 62: 12, 63: 11, 64: 10, 65: 13, 66: 20, 67: 7, 68: 35, 69: 36, 70: 5, 71: 24, 72: 20, 73: 28, 74: 23, 75: 10, 76: 12, 77: 20, 78: 72, 79: 13, 80: 19, 81: 16, 82: 8, 83: 18, 84: 12, 85: 13, 86: 17, 87: 7, 88: 18, 89: 52, 90: 17, 91: 16, 92: 15, 93: 5, 94: 23, 95: 11, 96: 13, 97: 12, 98: 9, 99: 9, 100: 5, 101: 8, 102: 28, 103: 22, 104: 35, 105: 45, 106: 48, 107: 43, 108: 13, 109: 31, 110: 7, 111: 10, 112: 10, 113: 9, 114: 8, 115: 18, 116: 19, 117: 2, 118: 29, 119: 176, 120: 7, 121: 8, 122: 9, 123: 4, 124: 8, 125: 5, 126: 6, 127: 5, 128: 6, 129: 8, 130: 8, 131: 3, 132: 18, 133: 3, 134: 3, 135: 21, 136: 26, 137: 9, 138: 8, 139: 24, 140: 13, 141: 10, 142: 7, 143: 12, 144: 15, 145: 21, 146: 10, 147: 20, 148: 14, 149: 9, 150: 6},
    "PRO": {1: 33, 2: 22, 3: 35, 4: 27, 5: 23, 6: 35, 7: 27, 8: 36, 9: 18, 10: 32, 11: 31, 12: 28, 13: 25, 14: 35, 15: 33, 16: 33, 17: 28, 18: 24, 19: 29, 20: 30, 21: 31, 22: 29, 23: 35, 24: 34, 25: 28, 26: 28, 27: 27, 28: 28, 29: 27, 30: 33, 31: 31},
    "JOB": {1: 22, 2: 13, 3: 26, 4: 21, 5: 27, 6: 30, 7: 21, 8: 22, 9: 35, 10: 22, 11: 20, 12: 25, 13: 28, 14: 22, 15: 35, 16: 22, 17: 16, 18: 21, 19: 29, 20: 29, 21: 34, 22: 30, 23: 17, 24: 25, 25: 6, 26: 14, 27: 23, 28: 28, 29: 25, 30: 31, 31: 40, 32: 22, 33: 33, 34: 37, 35: 16, 36: 33, 37: 24, 38: 41, 39: 30, 40: 24, 41: 34, 42: 17},
    "SNG": {1: 17, 2: 17, 3: 11, 4: 16, 5: 16, 6: 13, 7: 13, 8: 14},
    "RUT": {1: 22, 2: 23, 3: 18, 4: 22},
    "LAM": {1: 22, 2: 22, 3: 66, 4: 22, 5: 22},
    "ECC": {1: 18, 2: 26, 3: 22, 4: 17, 5: 20, 6: 12, 7: 29, 8: 17, 9: 18, 10: 20, 11: 10, 12: 14},
    "EST": {1: 22, 2: 23, 3: 15, 4: 17, 5: 14, 6: 14, 7: 10, 8: 17, 9: 32, 10: 3},
    "DAN": {1: 21, 2: 49, 3: 30, 4: 37, 5: 31, 6: 28, 7: 28, 8: 27, 9: 27, 10: 21, 11: 45, 12: 13},
    "EZR": {1: 11, 2: 70, 3: 13, 4: 24, 5: 17, 6: 22, 7: 28, 8: 36, 9: 15, 10: 44},
    "NEH": {1: 11, 2: 20, 3: 32, 4: 23, 5: 19, 6: 19, 7: 73, 8: 18, 9: 38, 10: 39, 11: 36, 12: 47, 13: 31},
    "1CH": {1: 54, 2: 55, 3: 24, 4: 43, 5: 41, 6: 81, 7: 40, 8: 40, 9: 44, 10: 14, 11: 47, 12: 40, 13: 14, 14: 17, 15: 29, 16: 43, 17: 27, 18: 17, 19: 19, 20: 8, 21: 30, 22: 19, 23: 32, 24: 31, 25: 31, 26: 32, 27: 34, 28: 21, 29: 30},
    "2CH": {1: 18, 2: 18, 3: 17, 4: 22, 5: 14, 6: 42, 7: 22, 8: 18, 9: 31, 10: 19, 11: 23, 12: 16, 13: 22, 14: 15, 15: 19, 16: 14, 17: 19, 18: 34, 19: 11, 20: 37, 21: 20, 22: 12, 23: 21, 24: 27, 25: 28, 26: 23, 27: 9, 28: 27, 29: 36, 30: 27, 31: 21, 32: 33, 33: 25, 34: 33, 35: 27, 36: 23}
}

# Lista padrão de livros como fallback
DEFAULT_BOOKS = [
    {"id": "GEN", "name": "Genesis", "namePortuguese": "Gênesis"},
    {"id": "EXO", "name": "Exodus", "namePortuguese": "Êxodo"},
    {"id": "LEV", "name": "Leviticus", "namePortuguese": "Levítico"},
    {"id": "NUM", "name": "Numbers", "namePortuguese": "Números"},
    {"id": "DEU", "name": "Deuteronomy", "namePortuguese": "Deuteronômio"},
    {"id": "JOS", "name": "Joshua", "namePortuguese": "Josué"},
    {"id": "JDG", "name": "Judges", "namePortuguese": "Juízes"},
    {"id": "1SA", "name": "1 Samuel", "namePortuguese": "1 Samuel"},
    {"id": "2SA", "name": "2 Samuel", "namePortuguese": "2 Samuel"},
    {"id": "1KI", "name": "1 Kings", "namePortuguese": "1 Reis"},
    {"id": "2KI", "name": "2 Kings", "namePortuguese": "2 Reis"},
    {"id": "ISA", "name": "Isaiah", "namePortuguese": "Isaías"},
    {"id": "JER", "name": "Jeremiah", "namePortuguese": "Jeremias"},
    {"id": "EZK", "name": "Ezekiel", "namePortuguese": "Ezequiel"},
    {"id": "HOS", "name": "Hosea", "namePortuguese": "Oséias"},
    {"id": "JOL", "name": "Joel", "namePortuguese": "Joel"},
    {"id": "AMO", "name": "Amos", "namePortuguese": "Amós"},
    {"id": "OBA", "name": "Obadiah", "namePortuguese": "Obadias"},
    {"id": "JON", "name": "Jonah", "namePortuguese": "Jonas"},
    {"id": "MIC", "name": "Micah", "namePortuguese": "Miquéias"},
    {"id": "NAM", "name": "Nahum", "namePortuguese": "Naum"},
    {"id": "HAB", "name": "Habakkuk", "namePortuguese": "Habacuque"},
    {"id": "ZEP", "name": "Zephaniah", "namePortuguese": "Sofonias"},
    {"id": "HAG", "name": "Haggai", "namePortuguese": "Ageu"},
    {"id": "ZEC", "name": "Zechariah", "namePortuguese": "Zacarias"},
    {"id": "MAL", "name": "Malachi", "namePortuguese": "Malaquias"},
    {"id": "PSA", "name": "Psalms", "namePortuguese": "Salmos"},
    {"id": "PRO", "name": "Proverbs", "namePortuguese": "Provérbios"},
    {"id": "JOB", "name": "Job", "namePortuguese": "Jó"},
    {"id": "SNG", "name": "Song of Solomon", "namePortuguese": "Cântico dos Cânticos"},
    {"id": "RUT", "name": "Ruth", "namePortuguese": "Rute"},
    {"id": "LAM", "name": "Lamentations", "namePortuguese": "Lamentações"},
    {"id": "ECC", "name": "Ecclesiastes", "namePortuguese": "Eclesiastes"},
    {"id": "EST", "name": "Esther", "namePortuguese": "Ester"},
    {"id": "DAN", "name": "Daniel", "namePortuguese": "Daniel"},
    {"id": "EZR", "name": "Ezra", "namePortuguese": "Esdras"},
    {"id": "NEH", "name": "Nehemiah", "namePortuguese": "Neemias"},
    {"id": "1CH", "name": "1 Chronicles", "namePortuguese": "1 Crônicas"},
    {"id": "2CH", "name": "2 Chronicles", "namePortuguese": "2 Crônicas"}
]

# Configurar sessão com retentativas
session = requests.Session()
retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[400, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)

# Função para listar os livros disponíveis
@cache.memoize(timeout=3600)  # Cache por 1 hora
def get_books():
    url = f"{BASE_URL}/bibles/{BIBLE_ID}/books"
    headers = {"accept": "application/json", "api-key": API_KEY}
    try:
        response = session.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "data" not in data:
            return [book["namePortuguese"] for book in DEFAULT_BOOKS]
        books = data["data"]
        for book in books:
            book["namePortuguese"] = BOOK_NAMES.get(book["id"], book["name"])
        return [book["namePortuguese"] for book in books]
    except requests.exceptions.RequestException as e:
        flash(f"Erro ao carregar livros: {str(e)}. Usando lista padrão.", "warning")
        return [book["namePortuguese"] for book in DEFAULT_BOOKS]

# Função para buscar uma faixa de versículos
@cache.memoize(timeout=86400)  # Cache por 24 horas
def get_verse(book_id, chapter, verse_start, verse_end):
    if not book_id or verse_start > verse_end or verse_start < 1:
        return []
    verses = []
    for verse_num in range(verse_start, verse_end + 1):
        verse_id = f"{book_id}.{chapter}.{verse_num}"
        url = f"{BASE_URL}/bibles/{BIBLE_ID}/verses/{verse_id}"
        params = {
            "content-type": "text",
            "include-notes": "false",
            "include-titles": "false",
            "include-chapter-numbers": "false",
            "include-verse-numbers": "true",
            "include-verse-spans": "false"
        }
        headers = {"accept": "application/json", "api-key": API_KEY}
        try:
            response = session.get(url, params=params, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            if "data" in data and "content" in data["data"]:
                content = data["data"]["content"]
                parsed_verses = parse_verse(content)
                if parsed_verses:
                    verses.extend(parsed_verses)
                else:
                    flash(f"Versículo {verse_id} retornou conteúdo vazio ou inválido.", "warning")
            else:
                flash(f"Resposta da API inválida para {verse_id}: {data}", "warning")
        except requests.exceptions.RequestException as e:
            flash(f"Erro ao carregar versículo {verse_id}: {str(e)}", "warning")
    return verses

# Função para parsear o versículo
def parse_verse(content):
    if not content:
        return []
    verse_pattern = re.compile(r'\[(\d+)\]\s*(.+?)(?=\[\d+\]|\Z)', re.DOTALL)
    matches = verse_pattern.finditer(content.strip())
    verses = []
    for match in matches:
        verse_number = int(match.group(1))
        verse_text = match.group(2).strip()
        verses.append({"verse": verse_number, "text": verse_text})
    return verses

# Função para obter o número total de capítulos em um livro
@cache.memoize(timeout=3600)  # Cache por 1 hora
def get_chapter_count(book):
    book_id = next((key for key, value in BOOK_NAMES.items() if value == book), None)
    if not book_id:
        flash(f"Livro {book} não encontrado. Usando número de capítulos padrão.", "warning")
        return CHAPTER_COUNTS.get(book_id, 1)
    return CHAPTER_COUNTS.get(book_id, 1)  # Usar mapeamento fixo para evitar chamada à API

# Função para obter o número total de versículos em um capítulo
@cache.memoize(timeout=3600)  # Cache por 1 hora
def get_verse_count(book, chapter):
    book_id = next((key for key, value in BOOK_NAMES.items() if value == book), None)
    if not book_id:
        return 1
    verse_count = VERSE_COUNTS.get(book_id, {}).get(chapter)
    if verse_count is None:
        flash(f"Número de versículos não mapeado para {book} capítulo {chapter}. Usando 1 como fallback.", "warning")
        return 1
    return verse_count

@bible_bp.route('/', methods=['GET'])
@login_required
def index():
    """Página inicial da Bíblia Hebraica."""
    books = get_books()
    if not books:
        books = [book["namePortuguese"] for book in DEFAULT_BOOKS]
    
    selected_book = request.args.get('book', books[0])
    if selected_book not in books:
        selected_book = books[0]
    
    chapter_count = get_chapter_count(selected_book)
    chapters = list(range(1, chapter_count + 1))
    
    selected_chapter = int(request.args.get('chapter', 1))
    if selected_chapter not in chapters:
        selected_chapter = 1
        flash(f"Capítulo {selected_chapter} inválido para {selected_book}. Ajustado para 1.", "warning")
    
    verse_count = get_verse_count(selected_book, selected_chapter)
    
    # Versículo inicial e final
    verse_start = int(request.args.get('verse_start', 1))
    verse_end = int(request.args.get('verse_end', verse_start))
    
    # Validações
    if verse_start < 1:
        verse_start = 1
        flash('Versículo inicial deve ser pelo menos 1.', 'warning')
    if verse_start > verse_count:
        verse_start = verse_count
        flash(f'Versículo inicial ajustado para o máximo ({verse_count}) para {selected_book} {selected_chapter}.', "warning")
    if verse_end < verse_start:
        verse_end = verse_start
        flash('Versículo final deve ser maior ou igual ao inicial.', 'warning')
    if verse_end > verse_count:
        verse_end = verse_count
        flash(f'Versículo final ajustado para o máximo ({verse_count}) para {selected_book} {selected_chapter}.', "warning")
    
    book_id = next((key for key, value in BOOK_NAMES.items() if value == selected_book), None)
    if not book_id:
        flash(f"Book ID não encontrado para! {selected_book}.", "warning")
        verses = []
    else:
        verses = get_verse(book_id, selected_chapter, verse_start, verse_end)
    if not verses:
        flash(f'Nenhum versículo encontrado para a faixa {selected_book} {selected_chapter}:{verse_start}-{verse_end}.', "warning")
    
    has_next_verse = verse_end < verse_count
    has_prev_verse = verse_start > 1
    
    return render_template('bible/index.html',
                          books=books,
                          chapters=chapters,
                          selected_book=selected_book,
                          selected_chapter=selected_chapter,
                          verse_start=verse_start,
                          verse_end=verse_end,
                          verses=verses,
                          has_next_verse=has_next_verse,
                          has_prev_verse=has_prev_verse,
                          verse_count=verse_count)