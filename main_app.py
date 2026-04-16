"""
Главный модуль приложения тестирования на Kivy.
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

# Импортируем наши экраны (их создадим далее)
from screens.start_screen import StartScreen
from screens.quiz_screen import QuizScreen
from screens.results_screen import ResultsScreen

# Импортируем сервисы core
from core.services.data_loader import DataLoader
from core.services.stats_manager import StatisticsManager
from core.services.quiz_scheduler import QuizScheduler
from core.utils.helpers import shuffle_options

class QuizApp(App):
    """
    Основной класс приложения Kivy.
    """

    def build(self):
        """
        Создаёт и возвращает root widget (ScreenManager).
        """
        sm = ScreenManager()

        # Инициализируем core-сервисы
        stats_manager = StatisticsManager()
        scheduler = QuizScheduler(stats_manager)
        data_loader = DataLoader()
        tests = data_loader.load_tests_from_directory()

        # Создаём и добавляем экраны в ScreenManager
        # Передаём им необходимые зависимости
        start_screen = StartScreen(name='start')
        start_screen.setup(tests, sm) # Передаём тесты и ScreenManager
        sm.add_widget(start_screen)

        quiz_screen = QuizScreen(name='quiz')
        # Передаём сервисы и ScreenManager
        quiz_screen.setup(stats_manager, scheduler, shuffle_options, sm)
        sm.add_widget(quiz_screen)

        results_screen = ResultsScreen(name='results')
        results_screen.setup(sm) # Передаём ScreenManager
        sm.add_widget(results_screen)

        # Устанавливаем начальный экран
        sm.current = 'start'
        return sm

if __name__ == '__main__':
    from kivy.config import Config

    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '600')
    Config.set('graphics', 'resizable', '1')  # Разрешить ресайз
    QuizApp().run()