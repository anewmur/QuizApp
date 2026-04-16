from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from core.utils.ui_theme import Theme, ModernLabel, ModernButton, CardLayout

class StartScreen(Screen):
    def setup(self, tests, screen_manager):
        self.tests = tests
        self.sm = screen_manager

        # Центрируем карту на экране
        self.root_anchor = AnchorLayout(anchor_x='center', anchor_y='center', padding=Theme.PADDING_OUTER)
        self.add_widget(self.root_anchor)

        # Белая карточка для списка тестов
        self.card = CardLayout()
        self.root_anchor.add_widget(self.card)

        # Заголовок внутри карты
        title = ModernLabel(text='Выберите тест:', is_title=True)
        self.card.add_widget(title)

        # Список тестов со скроллом
        scroll = ScrollView(size_hint_y=1)
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=Theme.SPACING)
        button_layout.bind(minimum_height=button_layout.setter('height'))

        for test in self.tests:
            btn = ModernButton(text=test.title, is_accent=False)
            btn.color = Theme.TEXT_MAIN # <-- ПРИНУДИТЕЛЬНО ЧЕРНЫЙ ТЕКСТ
            btn.bind(on_press=(lambda t: lambda instance: self.start_quiz(t))(test))
            button_layout.add_widget(btn)

        scroll.add_widget(button_layout)
        self.card.add_widget(scroll)

    def start_quiz(self, test):
        quiz_screen = self.sm.get_screen('quiz')
        quiz_screen.set_current_test(test)
        self.sm.current = 'quiz'