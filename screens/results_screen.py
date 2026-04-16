"""
Экран результатов теста.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp  # Для размеров


class ResultsScreen(Screen):
    """
    Экран, отображающий результаты пройденного теста.
    """

    def setup(self, screen_manager):
        """
        Инициализирует экран с ScreenManager.

        Args:
            screen_manager (ScreenManager): Экземпляр ScreenManager.
        """
        self.sm = screen_manager
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        self.result_label = Label(text='', size_hint_y=None, height=dp(50))
        self.detail_scroll = ScrollView()

        # Создаём detail_layout
        self.detail_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5), size_hint_x=1,
                                       padding=[dp(5)])  # size_hint_x=1 заставит его растягиваться по ширине родителя

        # Привязываем минимальную высоту к высоте самого layout (для ScrollView)
        self.detail_layout.bind(minimum_height=self.detail_layout.setter('height'))

        # Привязываем ширину detail_layout к ширине scroll_view
        self.detail_scroll.bind(width=self.detail_layout.setter('width'))

        self.detail_scroll.add_widget(self.detail_layout)

        back_button = Button(text='Назад к тестам', size_hint_y=None, height=dp(44))
        back_button.bind(on_press=self.go_back_to_start)

        self.layout.add_widget(self.result_label)
        self.layout.add_widget(self.detail_scroll)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def display_results(self, percentage: float, questions_data, test):
        """
        Отображает итоговый результат и детализацию.

        Args:
            percentage (float): Процент правильных ответов.
            questions_data (List[Question]): Список вопросов сессии.
            test (Test): Пройденный тест.
        """
        self.result_label.text = f'Тест "{test.title}" завершён!\nРезультат: {percentage:.2f}% ({int(percentage / 100 * len(questions_data))}/{len(questions_data)})'

        self.detail_layout.clear_widgets()

        #TODO: Это не самый чистый способ передачи данных, но для первого приближения сойдёт.
        # В идеале, статистику или её часть можно было бы передать напрямую в display_results,
        # или использовать шину событий/состояния. Но для простоты и скорости реализации, пусть пока будет так.

        for i, q in enumerate(questions_data):
            stats = self.sm.get_screen('quiz').stats_manager.get_question_stats(test.id, q.id)
            status = "Правильно" if stats['last_was_correct'] else "Неправильно"
            detail_text = f"{i + 1}. {q.text}\n[{status}]"

            # Создаём label
            detail_label = Label(
                text=detail_text,
                halign='left',
                valign='top',
                color=(0, 1, 0, 1) if stats['last_was_correct'] else (1, 0, 0, 1),
                size_hint_y=None,
                # text_size теперь будет привязан к ширине label, которую мы установим ниже
            )



            # Привязываем text_size к ширине самого label, чтобы текст переносился
            # Также вычтем отступы (padding), чтобы текст не упирался в края
            detail_label.bind(
                width=lambda lbl, w: setattr(lbl, 'text_size', (w - dp(10), None))
                # dp(10) как пример отступа, можно регулировать
            )

            self.detail_layout.add_widget(detail_label)

            # Опционально: вызываем texture_update, чтобы Kivy пересчитал размеры
            # detail_label.texture_update()

        # После добавления всех виджетов, вызываем пересчёт размеров у detail_layout
        # Это может помочь ScrollView корректно отработать
        self.detail_layout.height = self.detail_layout.minimum_height
    def go_back_to_start(self, instance):
        """
        Возвращается к экрану выбора теста.
        """
        self.sm.current = 'start'
