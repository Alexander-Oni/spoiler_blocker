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