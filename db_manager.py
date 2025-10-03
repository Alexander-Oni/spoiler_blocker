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