"""
Экран выбора теста.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class StartScreen(Screen):
    """
    Экран, отображающий список доступных тестов.
    """

    def setup(self, tests, screen_manager):
        """
        Инициализирует экран с тестами и устанавливает ScreenManager.

        Args:
            tests (List[Test]): Список тестов для отображения.
            screen_manager (ScreenManager): Экземпляр ScreenManager.
        """
        self.tests = tests
        self.sm = screen_manager
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title_label = Label(text='Выберите тест:', size_hint_y=None, height=50)
        self.layout.add_widget(title_label)

        scroll_view = ScrollView()
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        button_layout.bind(minimum_height=button_layout.setter('height'))

        for test in self.tests:
            btn = Button(text=test.title, size_hint_y=None, height=44)
            # Замыкание для захвата переменной test
            btn.bind(on_press=(lambda t: lambda instance: self.start_quiz(t))(test))
            button_layout.add_widget(btn)

        scroll_view.add_widget(button_layout)
        self.layout.add_widget(scroll_view)

        self.add_widget(self.layout)

    def start_quiz(self, test):
        """
        Переходит к экрану викторины, передавая выбранный тест.

        Args:
            test (Test): Выбранный тест.
        """
        quiz_screen = self.sm.get_screen('quiz')
        quiz_screen.set_current_test(test)
        self.sm.current = 'quiz'
