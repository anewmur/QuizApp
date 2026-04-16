from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', '1')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from core.utils.ui_theme import Theme
from screens.start_screen import StartScreen
from screens.quiz_screen import QuizScreen
from screens.results_screen import ResultsScreen
from core.services.data_loader import DataLoader
from core.services.stats_manager import StatisticsManager
from core.services.quiz_scheduler import QuizScheduler
from core.utils.helpers import shuffle_options

class QuizApp(App):
    def build(self):
        Window.clearcolor = Theme.BG_MILK
        sm = ScreenManager()
        stats_manager = StatisticsManager()
        scheduler = QuizScheduler(stats_manager)
        data_loader = DataLoader()
        tests = data_loader.load_tests_from_directory()

        sm.add_widget(StartScreen(name='start'))
        sm.get_screen('start').setup(tests, sm)

        sm.add_widget(QuizScreen(name='quiz'))
        sm.get_screen('quiz').setup(stats_manager, scheduler, shuffle_options, sm)

        sm.add_widget(ResultsScreen(name='results'))
        sm.get_screen('results').setup(sm)

        sm.current = 'start'
        return sm

if __name__ == '__main__':
    QuizApp().run()