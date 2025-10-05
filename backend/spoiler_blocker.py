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
    
# Точка входа в программу
if __name__ == "__main__":
  main()