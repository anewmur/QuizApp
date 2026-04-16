"""
Экран прохождения викторины.
Реализован современный дизайн, блок объяснения и навигация.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp

# Импортируем только нужные компоненты
from core.utils.ui_theme import (
    Theme,
    ModernLabel,
    ModernButton,
    OptionButton,
    CardLayout,
    ExplanationBox
)

class QuizScreen(Screen):
    def setup(self, stats_manager, scheduler, shuffle_func, screen_manager):
        self.stats_manager = stats_manager
        self.scheduler = scheduler
        self.shuffle_func = shuffle_func
        self.sm = screen_manager

        self.current_test = None
        self.session_questions = []
        self.current_index = 0
        self.selected_answer_button = None
        self.answer_locked = False

        # 1. Сначала создаем корневой слой и карту
        self.root_anchor = AnchorLayout(
            anchor_x='center',
            anchor_y='center',
            padding=Theme.PADDING_OUTER
        )
        self.add_widget(self.root_anchor)

        self.card = CardLayout()
        self.root_anchor.add_widget(self.card)

        # 2. Создаем элементы интерфейса

        # Кнопка "Назад"
        self.back_button = ModernButton(text='<-- К списку тестов', is_accent=False)
        self.back_button.height = dp(40)
        self.back_button.bind(on_press=self.go_back)

        # Индикатор прогресса
        self.progress_label = ModernLabel(
            text='',
            color=Theme.TEXT_DIM,
            font_size=Theme.NORMAL_FONT_SIZE - dp(2)
        )
        self.progress_label.height = dp(30)

        # Текст вопроса
        self.question_label = ModernLabel(text='', is_title=True)
        self.question_label.size_hint_y = None

        # Список вариантов (Scroll)
        self.scroll_view = ScrollView(size_hint_y=1, bar_width=dp(4))
        self.options_layout = BoxLayout(
            orientation='vertical',
            spacing=Theme.SPACING,
            size_hint_y=None
        )
        self.options_layout.bind(minimum_height=self.options_layout.setter('height'))
        self.scroll_view.add_widget(self.options_layout)

        # Блок объяснения (ExplanationBox)
        self.explanation_box = ExplanationBox()
        self.explanation_label = ModernLabel(text='', color=Theme.TEXT_MAIN, halign='left')
        self.explanation_box.add_widget(self.explanation_label)

        # Кнопка "Далее"
        self.next_button = ModernButton(text='Далее', is_accent=True, disabled=True)
        self.next_button.bind(on_press=self.go_to_next)

        # 3. Добавляем всё в карту в правильном порядке
        self.card.add_widget(self.back_button)
        self.card.add_widget(self.progress_label)
        self.card.add_widget(self.question_label)
        self.card.add_widget(self.scroll_view)
        self.card.add_widget(self.explanation_box)
        self.card.add_widget(self.next_button)



    def on_option_selected(self, instance):
        if self.answer_locked:
            return

        self.answer_locked = True
        current_q = self.session_questions[self.current_index]
        is_correct = instance.option_id in current_q.correct_option_ids

        for btn in self.options_layout.children:
            btn.is_answer_locked = 1  # Блокируем клики

            if btn.option_id in current_q.correct_option_ids:
                # Правильный ответ всегда зеленый блок
                btn.current_state_color = Theme.STATE_SUCCESS
            elif btn == instance and not is_correct:
                # Если выбрали неверный — он станет красным блоком
                btn.current_state_color = Theme.STATE_ERROR
            else:
                # Остальные — нейтральный светло-серый блок, текст останется читаемым
                btn.current_state_color = [0.9, 0.9, 0.9, 1]

        # Показ объяснения
        self.explanation_label.text = current_q.explanation
        self.explanation_box.opacity = 1
        self.explanation_label.texture_update()
        self.explanation_box.height = self.explanation_label.texture_size[1] + Theme.PADDING_INNER * 2

        self.stats_manager.update_question_stats(self.current_test.id, current_q.id, is_correct)
        self.next_button.disabled = False


    def show_current_question(self):
        """Сброс состояния при переходе к новому вопросу."""
        if self.current_index >= len(self.session_questions):
            self.finish_quiz()
            return

        self.answer_locked = False
        self.selected_answer_button = None
        question = self.session_questions[self.current_index]

        self.progress_label.text = f'ВОПРОС {self.current_index + 1} ИЗ {len(self.session_questions)}'
        self.question_label.text = question.text

        # Скрываем блок объяснения
        self.explanation_box.opacity = 0
        self.explanation_box.height = 0
        self.next_button.disabled = True

        self.question_label.texture_update()
        self.question_label.height = max(
            Theme.BTN_HEIGHT,
            self.question_label.texture_size[1] + Theme.SPACING * 2
        )

        self.options_layout.clear_widgets()
        shuffled_opts = self.shuffle_func(question.options)
        question.set_shuffled_options(shuffled_opts)

        for opt in shuffled_opts:
            btn = OptionButton(text=opt['text'])
            btn.option_id = opt['id']
            btn.bind(on_press=self.on_option_selected)
            self.options_layout.add_widget(btn)

    def go_back(self, instance):
        self.sm.current = 'start'

    def set_current_test(self, test):
        self.current_test = test
        self.session_questions = self.scheduler.get_questions_for_session(
            test.id, test.questions, mode="adaptive"
        )
        self.current_index = 0
        self.show_current_question()

    def go_to_next(self, instance):
        self.current_index += 1
        self.show_current_question()

    def finish_quiz(self):
        total = len(self.session_questions)
        correct = sum(1 for q in self.session_questions if
                      self.stats_manager.get_question_stats(self.current_test.id, q.id)['last_was_correct'])
        percentage = (correct / total) * 100 if total > 0 else 0

        results_screen = self.sm.get_screen('results')
        results_screen.display_results(percentage, self.session_questions, self.current_test)
        self.sm.current = 'results'