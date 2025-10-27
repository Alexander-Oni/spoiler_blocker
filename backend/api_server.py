"""
API ДЛЯ БРАУЗЕРНОГО РАСШИРЕНИЯ
Обеспечивает связь между расширением Chrome и базой данных PostgreSQL
"""

from flask import Flask, request, jsonify
from db_manager import DatabaseManager
from flask_cors import CORS  # Для разрешения запросов из браузера
import logging
import json

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

@app.before_request
def handle_preflight():
  if request.method == "OPTIONS":
    response = jsonify({"status": "success"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

@app.route('/')
def home():
  """Главная страница API сервера"""
  return jsonify({
    'message': 'SpoilerBlocker API Server',
    'version': '0.01',
    'endpoints': {
      '/api/keywords': 'GET - получить ключевые слова',
      '/api/block': 'POST - записать блокировку', 
      '/api/stats': 'GET - получить статистику'
    }
  })

@app.route('/api/keywords', methods=['GET', 'OPTIONS'])
def get_keywords():
  """
  API ЭНДПОИНТ: Получить все ключевые слова для расширения
  Вызывается при загрузке каждой страницы в браузере
  """
  if request.method == 'OPTIONS':
    return '', 200

  try:
    logger.info("Получен запрос на получение ключевых слов")
    
    # Получаем ключевые слова из базы данных
    keywords_data = db.get_all_keywords()
    
    # Преобразуем в формат JSON для JavaScript
    keywords_list = []
    for keyword in keywords_data:
        keyword_id, keyword_text, category_name, severity_level = keyword
        keywords_list.append({
          'id': keyword_id,
          'text': keyword_text,
          'category': category_name,
          'severity': severity_level
        })
    
    logger.info(f"Отправлено {len(keywords_list)} ключевых слов")
    
    response = jsonify({
      'success': True,
      'keywords': keywords_list,
      'count': len(keywords_list)
    })

    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response
  
  except Exception as e:
    logger.error(f"Ошибка в /api/keywords: {e}")
    return jsonify({
      'success': False, 
      'error': str(e)
    }), 500
  
@app.route('/api/block', methods=['POST', 'OPTIONS'])
def log_block():
  """
  API ЭНДПОИНТ: Записать факт блокировки спойлера
  Вызывается когда расширение блокирует спойлер на странице
  """

  if request.method == 'OPTIONS':
    return '', 200

  try:
    # Получаем JSON данные из запроса
    data = request.json
    logger.info(f"Получены данные блокировки: {data}")

    if not data:
      return jsonify({'success': False, 'error': 'No JSON data provided'}), 400
    
    keyword_text = data.get('keyword_text', '')
    
    if not keyword_text:
      return jsonify({'success': False, 'error': 'keyword_text is required'}), 400
    
    keyword_id = db.find_keyword_id_by_text(keyword_text)
    
    if not keyword_id:
      logger.warning(f"Ключевое слово не найдено: '{keyword_text}'")
      return jsonify({'success': False, 'error': 'Keyword not found'}), 404
    
    # Логируем блокировку в базу данных
    success = db.log_blocked_content(
      user_id = data.get('user_id', 1),  # По умолчанию user_id=1
      keyword_id = data.get('keyword_id'),
      url = data.get('url', ''),
      blocked_content = data.get('content', '')[:500]  # Ограничиваем длину
    )
    
    if success:
      logger.info("Блокировка записана в базу данных")
      return jsonify({'success': True})
    
    else:
      logger.error("Ошибка записи блокировки в БД")
      return jsonify({'success': False, 'error': 'Database error'})
  
  except Exception as e:
    logger.error(f"Ошибка в /api/block: {e}")
    return jsonify({
      'success': False, 
      'error': str(e)
    }), 500
  
@app.route('/api/stats', methods=['GET', 'OPTIONS'])
def get_stats():
  """
  API ЭНДПОИНТ: Получить статистику блокировок
  Используется во всплывающем окне расширения
  """

  if request.method == 'OPTIONS':
    return '', 200
  
  try:
    # Получаем user_id из параметров запроса
    user_id = request.args.get('user_id', 1, type=int)
    logger.info(f"Запрос статистики для пользователя {user_id}")
    
    # Получаем статистику из базы данных
    stats = db.get_user_stats(user_id)
    
    if stats:
      logger.info(f"Отправлена статистика: {stats}")
      return jsonify({
        'success': True, 
        'stats': stats
      })
    
    else:
      # Если статистики нет, возвращаем нули
      return jsonify({
        'success': True,
        'stats': {
          'total_blocks': 0,
          'unique_keywords_blocked': 0,
          'last_blocked': None
        }
      })
  
  except Exception as e:
    logger.error(f"Ошибка в /api/stats: {e}")
    return jsonify({
      'success': False, 
      'error': str(e)
    }), 500
  
@app.route('/api/health', methods=['GET'])
def health_check():
  """
  API ЭНДПОИНТ: Проверка здоровья сервера
  Используется для проверки доступности сервера
  """

  return jsonify({
    'status': 'healthy',
    'service': 'SpoilerBlocker API',
    'database': 'connected' if db.connection else 'disconnected'
  })

if __name__ == '__main__':
  print("Запуск SpoilerBLocker API сервера...")
  print("Адрес: http://localhost:5000")
  print("Доступные эндпоинты:")
  print("GET  /api/keywords - ключевые слова для блокировки")
  print("POST /api/block    - запись блокировки в лог") 
  print("GET  /api/stats    - статистика блокировок")
  print("GET  /api/health   - проверка здоровья сервера")
  print("\nСервер запущен. Для остановки нажмите Ctrl+C")
  
  # Запускаем Flask сервер
  app.run(
    host='localhost',  # Доступ только с локального компьютера
    port=5000,        # Порт для API сервера
    debug=True        # Режим отладки (выключить в продакшене)
  )