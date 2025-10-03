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

@app.route('/api/keywords', methods=['GET'])
def get_keywords():
  """
  API ЭНДПОИНТ: Получить все ключевые слова для расширения
  Вызывается при загрузке каждой страницы в браузере
  """

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
    
    return jsonify({
      'success': True,
      'keywords': keywords_list,
      'count': len(keywords_list)
    })
  
  except Exception as e:
    logger.error(f"❌ Ошибка в /api/keywords: {e}")
    return jsonify({
      'success': False, 
      'error': str(e)
    }), 500
  
@app.route('/api/block', methods=['POST'])
def log_block():
  """
  API ЭНДПОИНТ: Записать факт блокировки спойлера
  Вызывается когда расширение блокирует спойлер на странице
  """

  try:
    # Получаем JSON данные из запроса
    data = request.json
    logger.info(f"Получены данные блокировки: {data}")
    
    # Логируем блокировку в базу данных
    success = db.log_blocked_content(
      user_id = data.get('user_id', 1),  # По умолчанию user_id=1
      keyword_id = data.get('keyword_id'),
      url = data.get('url', ''),
      blocked_content = data.get('content', '')[:500]  # Ограничиваем длину
    )
    
    if success:
      logger.info("✅ Блокировка записана в базу данных")
      return jsonify({'success': True})
    
    else:
      logger.error("❌ Ошибка записи блокировки в БД")
      return jsonify({'success': False, 'error': 'Database error'})
  
  except Exception as e:
    logger.error(f"❌ Ошибка в /api/block: {e}")
    return jsonify({
      'success': False, 
      'error': str(e)
    }), 500
  
@app.route('/api/stats', methods=['GET'])
def get_stats():
  """
  API ЭНДПОИНТ: Получить статистику блокировок
  Используется во всплывающем окне расширения
  """

  try:
    # Получаем user_id из параметров запроса
    user_id = request.args.get('user_id', 1, type=int)
    logger.info(f"Запрос статистики для пользователя {user_id}")
    
    # Получаем статистику из базы данных
    stats = db.get_user_stats(user_id)
    
    if stats:
      logger.info(f" Отправлена статистика: {stats}")
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
    logger.error(f"❌ Ошибка в /api/stats: {e}")
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
  print("🚀 Запуск SpoilerShield API сервера...")
  print("📍 Адрес: http://localhost:5000")
  print("📚 Доступные эндпоинты:")
  print("   GET  /api/keywords - ключевые слова для блокировки")
  print("   POST /api/block    - запись блокировки в лог") 
  print("   GET  /api/stats    - статистика блокировок")
  print("   GET  /api/health   - проверка здоровья сервера")
  print("\n⚡ Сервер запущен. Для остановки нажмите Ctrl+C")
  
  # Запускаем Flask сервер
  app.run(
    host='localhost',  # Доступ только с локального компьютера
    port=5000,        # Порт для API сервера
    debug=True        # Режим отладки (выключить в продакшене)
  )