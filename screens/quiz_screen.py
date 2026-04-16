"""
Экран прохождения викторины.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

# Импорты для типизации (опционально, но рекомендуется)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.entities.test import Test
    from core.services.stats_manager import StatisticsManager
    from core.services.quiz_scheduler import QuizScheduler
    from core.utils.helpers import shuffle_options


class QuizScreen(Screen):
    """
    Экран, отображающий текущий вопрос и варианты ответов.
    """

    def setup(self, stats_manager, scheduler, shuffle_func, screen_manager):
        """
        Инициализирует экран с зависимостями.

        Args:
            stats_manager (StatisticsManager): Менеджер статистики.
            scheduler (QuizScheduler): Планировщик вопросов.
            shuffle_func (Callable): Функция для перемешивания опций.
            screen_manager (ScreenManager): Экземпляр ScreenManager.
        """
        self.stats_manager = stats_manager
        self.scheduler = scheduler
        self.shuffle_func = shuffle_func
        self.sm = screen_manager
        self.current_test = None
        self.session_questions = []
        self.current_index = 0
        self.selected_answer_button = None

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)

        # Элементы интерфейса
        self.progress_label = Label(text='', size_hint_y=None, height=40)
        self.question_label = Label(text='', halign='left', valign='top', size_hint_y=None)
        # Привязываем text_size к ширине label, а не к ширине родителя
        self.question_label.bind(width=self._update_question_text_size)

        self.options_layout = BoxLayout(orientation='vertical', spacing=5)
        self.options_layout.bind(minimum_height=self.options_layout.setter('height'))

        self.explanation_label = Label(text='', halign='left', valign='top', color=(0, 1, 0, 1), size_hint_y=None)
        self.explanation_label.bind(width=self._update_explanation_text_size)

        self.explanation_label.opacity = 0  # Скрыт по умолчанию

        self.next_button = Button(text='Далее', disabled=True)  # Отключен до выбора
        self.next_button.bind(on_press=self.go_to_next)

        # Добавляем элементы в layout
        self.layout.add_widget(self.progress_label)
        self.layout.add_widget(self.question_label)

        scroll_view_options = ScrollView()
        scroll_view_options.add_widget(self.options_layout)
        self.layout.add_widget(scroll_view_options)

        self.layout.add_widget(self.explanation_label)
        self.layout.add_widget(self.next_button)



    def _update_explanation_text_size(self, instance, width):
        """
        Обновляет text_size объяснения при изменении его ширины.
        """
        instance.text_size = (width, None)

    def set_current_test(self, test: 'Test'):
        """
        Устанавливает текущий тест и инициализирует сессию.

        Args:
            test (Test): Тест для запуска.
        """
        self.current_test = test
        # Получаем вопросы по алгоритму (например, adaptive)
        self.session_questions = self.scheduler.get_questions_for_session(test.id, test.questions, mode="adaptive")
        self.current_index = 0
        self.show_current_question()

    def _update_question_text_size(self, instance, width):
        """
        Обновляет text_size вопроса при изменении его ширины.
        """
        instance.text_size = (width, None)

    def show_current_question(self):
        """
        Отображает текущий вопрос и его опции.
        """
        if self.current_index >= len(self.session_questions):
            self.finish_quiz()
            return

        self.selected_answer_button = None
        question = self.session_questions[self.current_index]

        # Обновляем прогресс
        self.progress_label.text = f'Вопрос {self.current_index + 1} из {len(self.session_questions)}'

        # Обновляем текст вопроса
        self.question_label.text = question.text

        # Очищаем старые кнопки
        self.options_layout.clear_widgets()

        # Перемешиваем опции и сохраняем их состояние в объекте вопроса
        shuffled_opts = self.shuffle_func(question.options)
        question.set_shuffled_options(shuffled_opts)  # Сохраняем в объекте

        # Создаём и добавляем кнопки для опций
        for opt in shuffled_opts:
            btn = Button(text=opt['text'], size_hint_y=None, height=44)
            btn.option_id = opt['id']  # Привязываем ID опции к кнопке
            btn.bind(on_press=self.on_option_selected)
            self.options_layout.add_widget(btn)

        # Сбрасываем объяснение
        self.explanation_label.text = ''
        self.explanation_label.opacity = 0
        self.next_button.disabled = True

    def on_option_selected(self, instance):
        """
        Обрабатывает выбор варианта ответа.
        """
        if self.selected_answer_button:  # Убираем выделение с предыдущего
            self.selected_answer_button.background_color = [1, 1, 1, 1]  # Белый

        self.selected_answer_button = instance
        instance.background_color = [0.5, 0.7, 1, 1]  # Голубой

        # Проверяем ответ
        current_q = self.session_questions[self.current_index]
        is_correct = instance.option_id in current_q.correct_option_ids

        # Подсвечиваем правильный/неправильный ответ
        for btn in self.options_layout.children:
            if btn.option_id in current_q.correct_option_ids:
                btn.background_color = [0, 1, 0, 1]  # Зелёный для правильного
            elif btn == instance and not is_correct:
                btn.background_color = [1, 0, 0, 1]  # Красный для неправильного

        # Показываем объяснение
        self.explanation_label.text = current_q.explanation
        self.explanation_label.opacity = 1

        # Обновляем статистику
        self.stats_manager.update_question_stats(self.current_test.id, current_q.id, is_correct)

        # Активируем кнопку "Далее"
        self.next_button.disabled = False

    def go_to_next(self, instance):
        """
        Переходит к следующему вопросу.
        """
        self.current_index += 1
        self.show_current_question()

    def finish_quiz(self):
        """
        Завершает тест и переходит к экрану результатов.
        """
        # Подсчёт результата (примерный)
        total = len(self.session_questions)
        correct = sum(1 for q in self.session_questions if
                      self.stats_manager.get_question_stats(self.current_test.id, q.id)['last_was_correct'])
        percentage = (correct / total) * 100 if total > 0 else 0

        results_screen = self.sm.get_screen('results')
        results_screen.display_results(percentage, self.session_questions, self.current_test)
        self.sm.current = 'results'
