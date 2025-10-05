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

  def users_menu(self):
    """
    Меню для управления пользователями системы
    """

    while True:
      self.print_header("УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ")
      
      print(Fore.WHITE + "1.  Добавить нового пользователя")
      print(Fore.WHITE + "2.  Показать всех пользователей")
      print(Fore.WHITE + "3.  Назад в главное меню")
      print()
      
      choice = input(Fore.GREEN + " Выберите действие (1-3): ")
      
      if choice == "1":
        self.add_user()

      elif choice == "2":
        self.show_all_users()

      elif choice == "3":
        break

      else:
        print(Fore.RED + " Неверный выбор!")
        self.wait_for_enter()
  
  def add_user(self):
    """
    Форма для добавления нового пользователя
    """

    self.print_header("ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ")
    
    print(Fore.YELLOW + " Введите данные нового пользователя:")
    username = input(" Имя пользователя: ")
    email = input(" Email: ")
    
    # Выбор типа подписки
    print("\n Выберите тип подписки:")
    print("1.  Бесплатная")
    print("2.  Премиум")
    sub_choice = input("Выбор (1-2): ")
    
    subscription_type = "free" if sub_choice == "1" else "premium"
    
    # Проверяем, что все поля заполнены
    if username and email:
      self.db.add_user(username, email, subscription_type)

    else:
      print(Fore.RED + " Все поля должны быть заполнены!")
    
    self.wait_for_enter()
  
  def show_all_users(self):
    """
    Показывает список всех пользователей в системе
    """

    self.print_header("СПИСОК ПОЛЬЗОВАТЕЛЕЙ")
    
    users = self.db.get_all_users()
    if users:
      print(Fore.GREEN + f" Найдено пользователей: {len(users)}")
      print()
      print(Fore.CYAN + "ID  | Имя пользователя | Email              | Подписка")
      print(Fore.CYAN + "-" * 55)
      
      # Выводим каждого пользователя в формате таблицы
      for user in users:
        user_id, username, email, subscription = user
        sub_icon = "💎" if subscription == "premium" else "🆓"
        print(f"{user_id:3} | {username:15} | {email:18} | {sub_icon} {subscription}")

    else:
      print(Fore.YELLOW + "📭 Пользователи не найдены")
    
    self.wait_for_enter()