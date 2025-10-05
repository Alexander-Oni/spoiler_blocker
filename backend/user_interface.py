from colorama import Fore, Style, init
import os

# Инициализация цветного вывода в консоли
init(autoreset=True)

class UserInterface:
  def __init__(self, db_manager):
    """
    Конструктор - принимает объект для работы с базой данных
    """

    self.db = db_manager
  
  def clear_screen(self):
    """
    Очищает экран консоли 
    """

    os.system('cls' if os.name == 'nt' else 'clear')

  def print_header(self, title):
    """
    Выводит красивый заголовок 
    """

    self.clear_screen()
    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + f"SPOILER BLOCKER - {title}")
    print(Fore.CYAN + "=" * 60)
    print()
    
  def wait_for_enter(self):
    """
    Ожидает нажатия клавиши Enter для продолжения
    """

    input(Fore.YELLOW + "\n Нажмите Enter для продолжения...")

  def main_menu(self):
    """
    Главное меню системы
    """

    while True:
      self.print_header("ГЛАВНОЕ МЕНЮ")
      
      # Показываем все доступные опции
      print(Fore.WHITE + "1.  Управление пользователями")
      print(Fore.WHITE + "2.  Управление категориями")
      print(Fore.WHITE + "3.  Управление ключевыми словами")
      print(Fore.WHITE + "4.  Просмотр статистики")
      print(Fore.WHITE + "5.  Быстрая блокировка контента")
      print(Fore.RED + "0.  Выход из программы")
      print()
      
      # Получаем выбор пользователя
      choice = input(Fore.GREEN + " Выберите действие (0-5): ")
      
      # Обрабатываем выбор
      if choice == "1":
        self.users_menu()

      elif choice == "2":
        self.categories_menu()

      elif choice == "3":
        self.keywords_menu()

      elif choice == "4":
        self.statistics_menu()

      elif choice == "5":
        self.quick_block_menu()

      elif choice == "0":
        print(Fore.YELLOW + " До свидания!")
        break

      else:
        print(Fore.RED + " Неверный выбор! Попробуйте снова.")
        self.wait_for_enter()

  