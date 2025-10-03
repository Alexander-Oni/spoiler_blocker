import psycopg2
from psycopg2 import Error
from colorama import Fore, Style, init

# Инициализация библиотеки для цветного вывода
init(autoreset=True)

class DatabaseManager:

  def __init__(self, host='localhost', database='spoiler_blocker', 
                user='postgres', password='postgres'):
    """
    Конструктор класса - инициализирует подключение к базе данных
    """
    self.connection = None
    self.host = host
    self.database = database
    self.user = user
    self.password = password
    self.connect()

  def connect(self):
    """
    Устанавливает соединение с базой данных PostgreSQL
    """
    try:
      self.connection = psycopg2.connect(
          host=self.host,
          database=self.database,
          user=self.user,
          password=self.password,
          port=5432
      )
      print(Fore.GREEN + "✅ Успешное подключение к PostgreSQL")
      return True
    
    except Error as e:
      print(Fore.RED + f"❌ Ошибка подключения: {e}")
      print(Fore.YELLOW + "💡 Проверьте:")
      print("   - Запущен ли PostgreSQL сервер")
      print("   - Правильный ли пароль")
      print("   - Существует ли база данных 'spoiler_blocker'")
      return False
    
  def create_tables(self):
    """
    Создает все необходимые таблицы в базе данных
    Выполняет 5 SQL-запросов для создания таблиц
    """
    try:
      cursor = self.connection.cursor()
      
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
      print(Fore.GREEN + "✅ Все таблицы созданы успешно!")
      return True
        
    except Error as e:
      print(Fore.RED + f"❌ Ошибка создания таблиц: {e}")
      return False
      
  def add_user(self, username, email, subscription_type='free'):
    """
    Добавляет нового пользователя в систему
    """
    try:
      cursor = self.connection.cursor()
      query = "INSERT INTO Users (username, email, subscription_type) VALUES (%s, %s, %s)"
      cursor.execute(query, (username, email, subscription_type))
      self.connection.commit()
      print(Fore.GREEN + f"✅ Пользователь '{username}' добавлен!")
      return True
    
    except Error as e:
      print(Fore.RED + f"❌ Ошибка добавления пользователя: {e}")
      return False
    
  def get_all_users(self):
    """
    Получает список всех пользователей из базы данных
    """
    try:
      cursor = self.connection.cursor()
      cursor.execute("SELECT user_id, username, email, subscription_type FROM Users")
      return cursor.fetchall()
    
    except Error as e:
      print(Fore.RED + f"❌ Ошибка получения пользователей: {e}")
      return []
    
  def add_category(self, category_name, description):
    """
    Добавляет новую категорию контента (фильмы, сериалы и т.д.)
    """
    try:
      cursor = self.connection.cursor()
      query = "INSERT INTO Categories (category_name, description) VALUES (%s, %s)"
      cursor.execute(query, (category_name, description))
      self.connection.commit()
      print(Fore.GREEN + f"✅ Категория '{category_name}' добавлена!")
      return True
    
    except Error as e:
      print(Fore.RED + f"❌ Ошибка добавления категории: {e}")
      return False
  
  def get_all_categories(self):
    """
    Получает все активные категории из базы данных
    """
    try:
      cursor = self.connection.cursor()
      cursor.execute("SELECT category_id, category_name, description FROM Categories WHERE is_active = TRUE")
      return cursor.fetchall()
    
    except Error as e:
      print(Fore.RED + f"❌ Ошибка получения категорий: {e}")
      return []
        
  def add_keyword(self, keyword_text, category_id, severity_level='medium'):
    """
    Добавляет новое ключевое слово для блокировки
    """
    try:
      cursor = self.connection.cursor()
      query = "INSERT INTO Keywords (keyword_text, category_id, severity_level) VALUES (%s, %s, %s)"
      cursor.execute(query, (keyword_text, category_id, severity_level))
      self.connection.commit()
      print(Fore.GREEN + f"✅ Ключевое слово '{keyword_text}' добавлено!")
      return True
    
    except Error as e:
      print(Fore.RED + f"❌ Ошибка добавления ключевого слова: {e}")
      return False
      
  def get_all_keywords(self):
    """
    Получает все ключевые слова с информацией о категориях
    Использует SQL JOIN для объединения данных из двух таблиц
    """
    try:
      cursor = self.connection.cursor()
      query = """
      SELECT k.keyword_id, k.keyword_text, c.category_name, k.severity_level 
      FROM Keywords k 
      JOIN Categories c ON k.category_id = c.category_id
      """
      cursor.execute(query)
      return cursor.fetchall()
    
    except Error as e:
      print(Fore.RED + f"❌ Ошибка получения ключевых слов: {e}")
      return []