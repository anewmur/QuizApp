from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from core.utils.ui_theme import Theme, ModernLabel, ModernButton, CardLayout


class ResultsScreen(Screen):
    def setup(self, screen_manager):
        self.sm = screen_manager

        root_anchor = AnchorLayout(anchor_x='center', anchor_y='center', padding=Theme.PADDING_OUTER)
        self.add_widget(root_anchor)

        self.card = CardLayout()
        root_anchor.add_widget(self.card)

        self.result_label = ModernLabel(text='', is_title=True)
        self.card.add_widget(self.result_label)

        self.detail_scroll = ScrollView(size_hint_y=1)
        # Увеличили отступы (spacing) между вопросами, чтобы строки не слипались
        self.detail_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=Theme.SPACING)
        self.detail_layout.bind(minimum_height=self.detail_layout.setter('height'))
        self.detail_scroll.add_widget(self.detail_layout)
        self.card.add_widget(self.detail_scroll)

        back_button = ModernButton(text='Вернуться к списку тестов', is_accent=True)
        back_button.bind(on_press=self.go_back_to_start)
        self.card.add_widget(back_button)

    def display_results(self, percentage, questions_data, test):
        correct_count = int(percentage / 100 * len(questions_data))
        self.result_label.text = f'Тест завершён!\nРезультат: {percentage:.2f}% ({correct_count}/{len(questions_data)})'

        self.detail_layout.clear_widgets()

        for i, q in enumerate(questions_data):
            stats = self.sm.get_screen('quiz').stats_manager.get_question_stats(test.id, q.id)
            is_correct = stats['last_was_correct']

            # Формируем строку: Вопрос - [Результат]
            status_text = "Верно" if is_correct else "Ошибка"
            detail_text = f"{i + 1}. {q.text}  —  [{status_text}]"

            # Строго черный цвет и выравнивание по левому краю
            detail_label = ModernLabel(
                text=detail_text,
                color=Theme.TEXT_MAIN,
                halign='left'
            )
            detail_label.texture_update()
            detail_label.height = detail_label.texture_size[1] + Theme.SPACING
            self.detail_layout.add_widget(detail_label)

    def go_back_to_start(self, instance):
        self.sm.current = 'start'