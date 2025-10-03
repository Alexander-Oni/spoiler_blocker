"""
API ДЛЯ БРАУЗЕРНОГО РАСШИРЕНИЯ
Обеспечивает связь между расширением Chrome и базой данных PostgreSQL
"""

from flask import Flask, request, jsonify
from db_manager import DatabaseManager
from flask_cors import CORS  # Для разрешения запросов из браузера
import logging

# Настройка логирования для отладки
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем Flask приложение
app = Flask(__name__)
CORS(app)  # Разрешаем CORS запросы из браузера

# Инициализируем менеджер базы данных
db = DatabaseManager(
  host='localhost',
  database='spoiler_blocker', 
  user='postgres',
  password='postgres'  
)

