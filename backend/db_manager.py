import psycopg2
from psycopg2 import Error
from colorama import Fore, Style, init


# Инициализация библиотеки для цветного вывода
init(autoreset=True)

class DatabaseManager:

  def __init__(self, host='localhost', database='spoiler_blocker', 
              user='postgres', password='postgres', port=5432):
    """
    Конструктор класса - инициализирует подключение к базе данных
    """
    self.connection = None
    self.host = host
    self.database = database
    self.user = user
    self.password = password
    self.port = port
    self.is_connected=self.connect()

  def _ensure_connection(self):
    """Проверяет активность соединения с БД"""
    if not self.is_connected or self.connection is None or self.connection.closed:
      print(Fore.RED + "Нет активного подключения к базе данных")
      return False
    
    return True

  def connect(self):
    """
    Устанавливает соединение с базой данных PostgreSQL
    """
    if self.connection:
      self.connection.close()

    try:
      self.connection = psycopg2.connect(
        host=self.host,
        database=self.database,
        user=self.user,
        password=self.password,
        port=self.port
      )
      print(Fore.GREEN + "Успешное подключение к PostgreSQL")
      return True
    
    except Error as e:
      print(Fore.RED + f"Ошибка подключения: {e}")
      return False
    
  def create_tables(self):
    """
    Создает все необходимые таблицы в базе данных
    Выполняет 5 SQL-запросов для создания таблиц
    """
    if not self._ensure_connection():
      return False
    
    try:
      with self.connection.cursor() as cursor:
      
        # Список SQL-запросов для создания таблиц
        tables = [
          # Таблица пользователей
          """
          CREATE TABLE IF NOT EXISTS Users (
              user_id SERIAL PRIMARY KEY,
              username VARCHAR(50) UNIQUE NOT NULL,
              email VARCHAR(100) UNIQUE NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              subscription_type VARCHAR(20) DEFAULT 'free'
          )
          """,
          
          # Таблица категорий контента
          """
          CREATE TABLE IF NOT EXISTS Categories (
              category_id SERIAL PRIMARY KEY,
              category_name VARCHAR(100) NOT NULL,
              description TEXT,
              is_active BOOLEAN DEFAULT TRUE
          )
          """,
          
          # Таблица ключевых слов для блокировки
          """
          CREATE TABLE IF NOT EXISTS Keywords (
              keyword_id SERIAL PRIMARY KEY,
              keyword_text VARCHAR(200) NOT NULL,
              category_id INTEGER REFERENCES Categories(category_id),
              severity_level VARCHAR(20) DEFAULT 'medium',
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          )
          """,
          
          # Таблица связей пользователей и ключевых слов
          """
          CREATE TABLE IF NOT EXISTS User_Filters (
              filter_id SERIAL PRIMARY KEY,
              user_id INTEGER REFERENCES Users(user_id),
              keyword_id INTEGER REFERENCES Keywords(keyword_id),
              is_active BOOLEAN DEFAULT TRUE,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          )
          """,
          
          # Таблица для логирования блокировок
          """
          CREATE TABLE IF NOT EXISTS Blocked_Content_Log (
              log_id SERIAL PRIMARY KEY,
              user_id INTEGER REFERENCES Users(user_id),
              keyword_id INTEGER REFERENCES Keywords(keyword_id),
              url VARCHAR(500),
              blocked_content TEXT,
              blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          )
          """
        ]
        
        # Выполняем каждый SQL-запрос
        for table_query in tables:
          cursor.execute(table_query)
        
        # Сохраняем изменения в базе данных
        self.connection.commit()
        print(Fore.GREEN + "Все таблицы созданы успешно!")
        return True
        
    except Error as e:
      if self.connection:
        self.connection.rollback()

      print(Fore.RED + f"Ошибка создания таблиц: {e}")
      return False
      
  def add_user(self, username, email, subscription_type='free'):
    """
    Добавляет нового пользователя в систему
    """
    if not self._ensure_connection():
      return False

    try:
      with self.connection.cursor() as cursor:
        query = "INSERT INTO Users (username, email, subscription_type) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, subscription_type))
        self.connection.commit()
        print(Fore.GREEN + f"Пользователь '{username}' добавлен!")
        return True
    
    except Error as e:
      if self.connection:
        self.connection.rollback()

      print(Fore.RED + f"Ошибка добавления пользователя: {e}")
      return False
    
  def get_all_users(self):
    """
    Получает список всех пользователей из базы данных
    """

    if not self._ensure_connection():
      return []
    
    try:
      with self.connection.cursor() as cursor:
        cursor.execute("SELECT user_id, username, email, subscription_type FROM Users")
        return cursor.fetchall()
    
    except Error as e:
      print(Fore.RED + f"Ошибка получения пользователей: {e}")
      return []
    
  def add_category(self, category_name, description):
    """
    Добавляет новую категорию контента (фильмы, сериалы и т.д.)
    """

    if not self._ensure_connection():
      return False
    
    try:
      with self.connection.cursor() as cursor:
        query = "INSERT INTO Categories (category_name, description) VALUES (%s, %s)"
        cursor.execute(query, (category_name, description))
        self.connection.commit()
        print(Fore.GREEN + f"Категория '{category_name}' добавлена!")
        return True
    
    except Error as e:
      if self.connection:
        self.connection.rollback()

      print(Fore.RED + f"Ошибка добавления категории: {e}")
      return False
  
  def get_all_categories(self):
    """
    Получает все активные категории из базы данных
    """

    if not self._ensure_connection():
      return []
    
    try:
      with self.connection.cursor() as cursor:
        cursor.execute("SELECT category_id, category_name, description FROM Categories WHERE is_active = TRUE")
        return cursor.fetchall()
    
    except Error as e:
      print(Fore.RED + f"Ошибка получения категорий: {e}")
      return []
        
  def add_keyword(self, keyword_text, category_id, severity_level='medium'):
    """
    Добавляет новое ключевое слово для блокировки
    """

    if not self._ensure_connection():
      return False
    
    try:
      with self.connection.cursor() as cursor:
        query = "INSERT INTO Keywords (keyword_text, category_id, severity_level) VALUES (%s, %s, %s)"
        cursor.execute(query, (keyword_text, category_id, severity_level))
        self.connection.commit()
        print(Fore.GREEN + f"Ключевое слово '{keyword_text}' добавлено!")
        return True
    
    except Error as e:
      if self.connection:
        self.connection.rollback()

      print(Fore.RED + f"Ошибка добавления ключевого слова: {e}")
      return False
      
  def get_all_keywords(self):
    """
    Получает все ключевые слова с информацией о категориях
    Использует SQL JOIN для объединения данных из двух таблиц
    """

    if not self._ensure_connection():
      return []
    
    try:
      with self.connection.cursor() as cursor:
        query = """
        SELECT k.keyword_id, k.keyword_text, c.category_name, k.severity_level 
        FROM Keywords k 
        JOIN Categories c ON k.category_id = c.category_id
        """
        cursor.execute(query)
        return cursor.fetchall()
    
    except Error as e:
      print(Fore.RED + f"Ошибка получения ключевых слов: {e}")
      return []
    
  def search_keywords(self, search_term):
    """
    Ищет ключевые слова по тексту (поиск с частичным совпадением)
    """

    if not self._ensure_connection():
      return []
    
    try:
      with self.connection.cursor() as cursor:
        query = "SELECT keyword_id, keyword_text FROM Keywords WHERE keyword_text ILIKE %s"
        cursor.execute(query, (f'%{search_term}%',))
        return cursor.fetchall()
    
    except Error as e:
      print(Fore.RED + f"Ошибка поиска: {e}")
      return []
      
  def delete_keyword(self, keyword_id):
    """
    Удаляет ключевое слово из системы
    Сначала удаляет связанные данные из других таблиц
    """

    if not self._ensure_connection():
      return False
    
    try:
      with self.connection.cursor() as cursor:
        # Удаляем связи с пользователями
        cursor.execute("DELETE FROM User_Filters WHERE keyword_id = %s", (keyword_id,))
        # Удаляем записи из лога
        cursor.execute("DELETE FROM Blocked_Content_Log WHERE keyword_id = %s", (keyword_id,))
        # Удаляем само ключевое слово
        cursor.execute("DELETE FROM Keywords WHERE keyword_id = %s", (keyword_id,))
        
        self.connection.commit()
        print(Fore.GREEN + "Ключевое слово удалено!")
        return True
    
    except Error as e:
      if self.connection:
        self.connection.rollback()
      print(Fore.RED + f"Ошибка удаления: {e}")
      return False
    
  def find_keyword_id_by_text(self, keyword_text):
    """Поиск ID ключевого слова по тексту"""

    try:
      with self.connection.cursor() as cursor:
        query = "SELECT keyword_id FROM Keywords WHERE keyword_text = %s"
        cursor.execute(query, (keyword_text,))
        result = cursor.fetchone()
          
        if result:
          keyword_id = result[0]
          print(f"[OK] Найден keyword_id {keyword_id} для '{keyword_text}'")
          return keyword_id
        
        else:
          print(f"[WARN] Ключевое слово '{keyword_text}' не найдено в базе")
          return None
      
    except Error as e:
        print(Fore.RED + f"[ERROR] Ошибка поиска keyword_id: {e}")
        return None
    
  def log_blocked_content(self, user_id, keyword_id, url, blocked_content):
    """
    Записывает информацию о блокировке контента в лог
    """

    if not self._ensure_connection():
      return False
    
    try:
      with self.connection.cursor() as cursor:
        query = "INSERT INTO Blocked_Content_Log (user_id, keyword_id, url, blocked_content) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, keyword_id, url, blocked_content))
        self.connection.commit()
        return True
    
    except Error as e:
      if self.connection:
        self.connection.rollback()

      print(Fore.RED + f"Ошибка логирования: {e}")
      return False
    
  def get_user_stats(self, user_id):
    """
    Получает статистику блокировок для конкретного пользователя
    """

    if not self._ensure_connection():
      return None
    
    try:
      with self.connection.cursor() as cursor:
        query = """
        SELECT 
          COUNT(*) as total_blocks,
          COUNT(DISTINCT keyword_id) as unique_keywords_blocked,
          MAX(blocked_at) as last_blocked
        FROM Blocked_Content_Log 
        WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        
        if result:
          return {
            'total_blocks': result[0],
            'unique_keywords_blocked': result[1],
            'last_blocked': result[2]
          }
        return None
    
    except Error as e:
      print(Fore.RED + f"Ошибка получения статистики: {e}")
      return None
    
  def get_popular_keywords(self, limit=10):
    """
    Получает самые популярные ключевые слова по количеству блокировок
    """

    if not self._ensure_connection():
      return []
    
    try:
      with self.connection.cursor() as cursor:
        query = """
          SELECT k.keyword_text, COUNT(b.keyword_id) as block_count
          FROM Keywords k
          LEFT JOIN Blocked_Content_Log b ON k.keyword_id = b.keyword_id
          GROUP BY k.keyword_id, k.keyword_text
          ORDER BY block_count DESC
          LIMIT %s
        """
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        
        popular_keywords = []
        for row in results:
          popular_keywords.append({
            'keyword_text': row[0],
            'block_count': row[1]
          })
        return popular_keywords
    
    except Error as e:
      print(Fore.RED + f"Ошибка получения популярных слов: {e}")
      return []
    
  def close_connection(self):
    """
    Закрывает соединение с базой данных
    """
    if self.connection:
      self.connection.close()
      print(Fore.BLUE + "Соединение с базой данных закрыто")