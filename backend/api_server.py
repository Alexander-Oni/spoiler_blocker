from flask import Flask, request, jsonify
from db_manager import DatabaseManager
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# НАСТРОЙКА CORS - ТОЛЬКО ОДИН РАЗ
CORS(app, resources={
  r"/api/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization", "Accept"]
  }
})

db = DatabaseManager(
  host='localhost',
  database='spoiler_blocker', 
  user='postgres',
  password='postgres'
)

@app.route('/')
def home():
  return jsonify({
    'message': 'SpoilerBlocker API Server',
    'version': '2.0',
    'endpoints': {
      '/api/keywords': 'GET - получить ключевые слова',
      '/api/block': 'POST - записать блокировку', 
      '/api/stats': 'GET - получить статистику'
    }
  })

@app.route('/api/keywords', methods=['GET'])
def get_keywords():
  try:
    logger.info("Получен запрос на получение ключевых слов")
    
    keywords_data = db.get_all_keywords()
    
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
    
    return response
  
  except Exception as e:
      logger.error(f"Ошибка в /api/keywords: {e}")
      return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/block', methods=['POST'])
def log_block():
  try:
    data = request.get_json()
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
    
    success = db.log_blocked_content(
      user_id=data.get('user_id', 1),
      keyword_id=keyword_id,
      url=data.get('url', ''),
      blocked_content=data.get('content', '')[:500]
    )
    
    if success:
      logger.info(f"Блокировка записана: '{keyword_text}' (ID: {keyword_id})")
      return jsonify({'success': True})
    
    else:
      logger.error("Ошибка записи блокировки в БД")
      return jsonify({'success': False, 'error': 'Database error'})
  
  except Exception as e:
    logger.error(f"Ошибка в /api/block: {e}")
    return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
  try:
    user_id = request.args.get('user_id', 1, type=int)
    logger.info(f"Запрос статистики для пользователя {user_id}")
    
    stats = db.get_user_stats(user_id)
    
    if stats:
      logger.info(f"Отправлена статистика: {stats}")
      return jsonify({'success': True, 'stats': stats})
    
    else:
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
    return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
  return jsonify({
    'status': 'healthy',
    'service': 'SpoilerBlocker API',
    'database': 'connected' if db.connection else 'disconnected'
  })

if __name__ == '__main__':
  print("Запуск SpoilerBlocker API сервера...")
  print("Адрес: http://localhost:5000")
  print("Сервер запущен. Для остановки нажмите Ctrl+C")
  
  app.run(host='localhost', port=5000, debug=True)