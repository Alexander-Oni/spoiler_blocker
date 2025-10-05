#!/usr/bin/env python3
"""
SPOILER BLOCKER - Система блокировки спойлеров
Главный файл программы

Автор: Онищенко Алксандр
Группа: 243-323
Дата: 05.10.2025
"""

# Импортируем необходимые модули
from db_manager import DatabaseManager
from user_interface import UserInterface
from colorama import Fore, Style, init
import sys

# Инициализируем библиотеку для цветного вывода
init(autoreset=True)

def main():
  """
  Главная функция программы - точка входа в приложение
  """

  # Выводим красивый заголовок
  print(Fore.CYAN + """
  ********************************************
  *         SPOILER BLOCKER v0.01            *
  *   Система блокировки спойлеров           *
  ********************************************
  """)
  
  print(Fore.YELLOW + "         Система блокировки спойлеров v0.01")
  print(Fore.CYAN + "=" * 50)
  print()

  # Запрашиваем параметры подключения у пользователя
  host = input("Хост (localhost): ") or "localhost"
  database = input("База данных (spoiler_blocker): ") or "spoiler_blocker"
  user = input("Пользователь (postgres): ") or "postgres"
  password = input("Пароль: ") or "postgres"

  print()
  print(Fore.YELLOW + "Подключаемся к базе данных...")

  try:
    # Создаем менеджер базы данных
    db_manager = DatabaseManager(host, database, user, password)
    
    # Проверяем подключение
    if not db_manager.connect():
      print(Fore.RED + "Не удалось подключиться к базе данных!")
      print(Fore.YELLOW + "Решение проблем:")
      print("1. Убедитесь, что PostgreSQL запущен")
      print("2. Проверьте правильность пароля")
      print("3. Создайте базу данных 'spoiler_blocker'")
      sys.exit(1)
    
    # Создаем таблицы в базе данных
    print(Fore.YELLOW + "Проверяем структуру базы данных...")
    db_manager.create_tables()
    
    # Система готова к работе
    print(Fore.GREEN + "Система готова к работе!")
    print()
    
    # Создаем и запускаем пользовательский интерфейс
    ui = UserInterface(db_manager)
    ui.main_menu()

  except KeyboardInterrupt:
    print(Fore.YELLOW + "\n\nПрограмма прервана пользователем")

  except Exception as e:
    print(Fore.RED + f"\nКритическая ошибка: {e}")

  finally:
    if 'db_manager' in locals():
      db_manager.close_connection()
    
    print(Fore.CYAN + "\n" + "=" * 50)
    print(Fore.YELLOW + "Спасибо за использование SpoilerBlocker!")
    print(Fore.CYAN + "=" * 50)
    
# Точка входа в программу
if __name__ == "__main__":
  main()