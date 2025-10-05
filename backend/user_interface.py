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

    input(Fore.YELLOW + "\nНажмите Enter для продолжения...")

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
      print(Fore.RED + "0.  Выход из программы")
      print()
      
      # Получаем выбор пользователя
      choice = input(Fore.GREEN + "Выберите действие (0-5): ")
      
      # Обрабатываем выбор
      if choice == "1":
        self.users_menu()

      elif choice == "2":
        self.categories_menu()

      elif choice == "3":
        self.keywords_menu()

      elif choice == "4":
        self.statistics_menu()

      elif choice == "0":
        print(Fore.YELLOW + "До свидания!")
        break

      else:
        print(Fore.RED + "Неверный выбор! Попробуйте снова.")
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
      
      choice = input(Fore.GREEN + "Выберите действие (1-3): ")
      
      if choice == "1":
        self.add_user()

      elif choice == "2":
        self.show_all_users()

      elif choice == "3":
        break

      else:
        print(Fore.RED + "Неверный выбор!")
        self.wait_for_enter()
  
  def add_user(self):
    """
    Форма для добавления нового пользователя
    """

    self.print_header("ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ")
    
    print(Fore.YELLOW + "Введите данные нового пользователя:")
    username = input("Имя пользователя: ")
    email = input("Email: ")
    
    # Выбор типа подписки
    print("\nВыберите тип подписки:")
    print("1.  Бесплатная")
    print("2.  Премиум")
    sub_choice = input("Выбор (1-2): ")
    
    subscription_type = "free" if sub_choice == "1" else "premium"
    
    # Проверяем, что все поля заполнены
    if username and email:
      self.db.add_user(username, email, subscription_type)

    else:
      print(Fore.RED + "Все поля должны быть заполнены!")
    
    self.wait_for_enter()
  
  def show_all_users(self):
    """
    Показывает список всех пользователей в системе
    """

    self.print_header("СПИСОК ПОЛЬЗОВАТЕЛЕЙ")
    
    users = self.db.get_all_users()
    if users:
      print(Fore.GREEN + f"Найдено пользователей: {len(users)}")
      print()
      print(Fore.CYAN + "ID  | Имя пользователя | Email              | Подписка")
      print(Fore.CYAN + "-" * 55)
      
      # Выводим каждого пользователя в формате таблицы
      for user in users:
        user_id, username, email, subscription = user
        sub_icon = "PREM" if subscription == "premium" else "FREE"
        print(f"{user_id:3} | {username:15} | {email:18} | {sub_icon} {subscription}")

    else:
      print(Fore.YELLOW + "Пользователи не найдены")
    
    self.wait_for_enter()

  def categories_menu(self):
    """
    Меню для управления категориями контента
    """

    while True:
      self.print_header("УПРАВЛЕНИЕ КАТЕГОРИЯМИ")
      
      print(Fore.WHITE + "1.  Добавить новую категорию")
      print(Fore.WHITE + "2.  Показать все категории")
      print(Fore.WHITE + "3.  Назад в главное меню")
      print()
      
      choice = input(Fore.GREEN + "Выберите действие (1-3): ")
      
      if choice == "1":
        self.add_category()

      elif choice == "2":
        self.show_all_categories()

      elif choice == "3":
        break

      else:
        print(Fore.RED + "Неверный выбор!")
        self.wait_for_enter()
  
  def add_category(self):
    """
    Форма для добавления новой категории
    """

    self.print_header("ДОБАВЛЕНИЕ КАТЕГОРИИ")
    
    print(Fore.YELLOW + "Введите данные новой категории:")
    category_name = input("Название категории: ")
    description = input("Описание: ")
    
    if category_name:
      self.db.add_category(category_name, description)

    else:
      print(Fore.RED + "Название категории обязательно!")
    
    self.wait_for_enter()
  
  def show_all_categories(self):
    """
    Показывает все категории контента
    """

    self.print_header("СПИСОК КАТЕГОРИЙ")
    
    categories = self.db.get_all_categories()
    if categories:
      print(Fore.GREEN + f"Найдено категорий: {len(categories)}")
      print()

      for category in categories:
        category_id, category_name, description = category
        print(f"   {category_id}. {category_name} - {description}")

    else:
      print(Fore.YELLOW + "Категории не найдены")
    
    self.wait_for_enter()

  def keywords_menu(self):
    """
    Меню для управления ключевыми словами
    """

    while True:
      self.print_header("УПРАВЛЕНИЕ КЛЮЧЕВЫМИ СЛОВАМИ")
      
      print(Fore.WHITE + "1.  Добавить новое ключевое слово")
      print(Fore.WHITE + "2.  Показать все ключевые слова")
      print(Fore.WHITE + "3.  Поиск ключевых слов")
      print(Fore.WHITE + "4.  Удалить ключевое слово")
      print(Fore.WHITE + "5.  Назад в главное меню")
      print()
      
      choice = input(Fore.GREEN + "Выберите действие (1-5): ")
      
      if choice == "1":
        self.add_keyword()

      elif choice == "2":
        self.show_all_keywords()

      elif choice == "3":
        self.search_keywords()

      elif choice == "4":
        self.delete_keyword()

      elif choice == "5":
        break

      else:
        print(Fore.RED + "Неверный выбор!")
        self.wait_for_enter()
    
  def add_keyword(self):
    """
    Форма для добавления нового ключевого слова
    """

    self.print_header("ДОБАВЛЕНИЕ КЛЮЧЕВОГО СЛОВА")
    
    # Сначала показываем доступные категории
    categories = self.db.get_all_categories()
    if not categories:
      print(Fore.RED + "Сначала добавьте категории!")
      self.wait_for_enter()
      return
    
    print(Fore.YELLOW + "Доступные категории:")
    for category in categories:
      category_id, category_name, description = category
      print(f"   {category_id}. {category_name}")
    print()
    
    try:
      # Получаем данные от пользователя
      category_id = int(input("Выберите ID категории: "))
      keyword_text = input("Ключевое слово/фраза: ")
      
      # Выбор уровня серьезности
      print("\n Уровень серьезности:")
      print("1. RED Высокий (критические спойлеры)")
      print("2. YELLOW Средний (важные детали сюжета)") 
      print("3. GREEN Низкий (незначительные спойлеры)")
      severity_choice = input("Выбор (1-3): ")
      
      # Преобразуем выбор в текстовое значение
      severity_map = {"1": "high", "2": "medium", "3": "low"}
      severity_level = severity_map.get(severity_choice, "medium")
      
      # Проверяем и добавляем ключевое слово
      if keyword_text and category_id:
        self.db.add_keyword(keyword_text, category_id, severity_level)

      else:
        print(Fore.RED + "Все поля должны быть заполнены!")

    except ValueError:
      print(Fore.RED + "ID категории должен быть числом!")
    
    self.wait_for_enter()
  
  def show_all_keywords(self):
    """
    Показывает все ключевые слова с детальной информацией
    """

    self.print_header("ВСЕ КЛЮЧЕВЫЕ СЛОВА")
    
    keywords = self.db.get_all_keywords()
    if keywords:
      print(Fore.GREEN + f"Найдено ключевых слов: {len(keywords)}")
      print()
      for keyword in keywords:
        keyword_id, keyword_text, category_name, severity_level = keyword
        # Выбираем emoji в зависимости от уровня серьезности
        severity_icon = "RED" if severity_level == "high" else "YELLOW" if severity_level == "medium" else "GREEN"
        print(f"   {keyword_id}. {keyword_text} ({category_name}) {severity_icon}")

    else:
      print(Fore.YELLOW + "Ключевые слова не найдены")
    
    self.wait_for_enter()
  
  def search_keywords(self):
    """
    Поиск ключевых слов по частичному совпадению
    """

    self.print_header("ПОИСК КЛЮЧЕВЫХ СЛОВ")
    
    search_term = input("Введите текст для поиска: ")
    if search_term:
      results = self.db.search_keywords(search_term)

      if results:
        print(Fore.GREEN + f"Найдено результатов: {len(results)}")
        print()

        for keyword_id, keyword_text in results:
          print(f"   {keyword_id}. {keyword_text}")

      else:
        print(Fore.YELLOW + "Ничего не найдено")

    else:
      print(Fore.RED + "Введите текст для поиска!")
    
    self.wait_for_enter()
  
  def delete_keyword(self):
    """
    Удаление ключевого слова из системы
    """

    self.print_header("УДАЛЕНИЕ КЛЮЧЕВОГО СЛОВА")
    
    keywords = self.db.get_all_keywords()
    if not keywords:
      print(Fore.YELLOW + "Нет ключевых слов для удаления")
      self.wait_for_enter()
      return
    
    print(Fore.YELLOW + "Доступные ключевые слова:")
    for keyword in keywords:
      keyword_id, keyword_text, category_name, severity_level = keyword
      print(f"   {keyword_id}. {keyword_text} ({category_name})")
    print()
    
    try:
      keyword_id = int(input("Введите ID ключевого слова для удаления: "))
      confirm = input("Вы уверены? (y/N): ")

      if confirm.lower() == 'y':
          self.db.delete_keyword(keyword_id)

      else:
          print(Fore.YELLOW + "Удаление отменено")

    except ValueError:
      print(Fore.RED + "ID должен быть числом!")
    
    self.wait_for_enter()

  def statistics_menu(self):
    """
    Меню для просмотра статистики системы
    """

    while True:
      self.print_header("СТАТИСТИКА СИСТЕМЫ")
      
      print(Fore.WHITE + "1.  Общая статистика")
      print(Fore.WHITE + "2.  Популярные ключевые слова")
      print(Fore.WHITE + "3.  Статистика по пользователю")
      print(Fore.WHITE + "4.  Назад в главное меню")
      print()
      
      choice = input(Fore.GREEN + "Выберите действие (1-4): ")
      
      if choice == "1":
        self.show_general_stats()

      elif choice == "2":
        self.show_popular_keywords()

      elif choice == "3":
        self.show_user_stats()

      elif choice == "4":
        break

      else:
        print(Fore.RED + "Неверный выбор!")
        self.wait_for_enter()

  def show_general_stats(self):
    """
    Показывает общую статистику системы
    """

    self.print_header("ОБЩАЯ СТАТИСТИКА")
    
    # Получаем все данные для статистики
    users = self.db.get_all_users()
    categories = self.db.get_all_categories()
    keywords = self.db.get_all_keywords()
    
    print(Fore.GREEN + "Общая статистика системы:")
    print()
    print(f"Пользователей: {len(users)}")
    print(f"Категорий: {len(categories)}")
    print(f"Ключевых слов: {len(keywords)}")
    print()  
    
    self.wait_for_enter()

  def show_popular_keywords(self):
    """
    Показывает самые популярные ключевые слова
    """

    self.print_header("ПОПУЛЯРНЫЕ КЛЮЧЕВЫЕ СЛОВА")
    
    try:
      limit = int(input("Сколько ключевых слов показать? (по умолчанию 10): ") or "10")
      popular_keywords = self.db.get_popular_keywords(limit)
      
      if popular_keywords:
        print()
        print(Fore.GREEN + f"Топ-{len(popular_keywords)} популярных ключевых слов:")
        print()

        for i, item in enumerate(popular_keywords, 1):
          print(f"{i:2}. {item['keyword_text']} - {item['block_count']} блокировок")

      else:
        print(Fore.YELLOW + "Нет данных о блокировках")

    except ValueError:
      print(Fore.RED + "Введите число!")
    
    self.wait_for_enter()

  def show_user_stats(self):
    """
    Показывает статистику для конкретного пользователя
    """

    self.print_header("СТАТИСТИКА ПОЛЬЗОВАТЕЛЯ")
    
    users = self.db.get_all_users()
    if not users:
      print(Fore.YELLOW + "Нет пользователей в системе")
      self.wait_for_enter()
      return
    
    print(Fore.YELLOW + "Доступные пользователи:")
    for user in users:
      user_id, username, email, subscription = user
      print(f"   {user_id}. {username} ({email})")
    print()
    
    try:
      user_id = int(input("Введите ID пользователя: "))
      stats = self.db.get_user_stats(user_id)
      
      if stats:
        print()
        print(Fore.GREEN + f"Статистика пользователя ID {user_id}:")
        print(f"Всего блокировок: {stats['total_blocks']}")
        print(f"Уникальных слов: {stats['unique_keywords_blocked']}")
        print(f"Последняя блокировка: {stats['last_blocked'] or 'никогда'}")

      else:
        print(Fore.YELLOW + f"Нет статистики для пользователя ID {user_id}")

    except ValueError:
      print(Fore.RED + "ID должен быть числом!")
    
    self.wait_for_enter()