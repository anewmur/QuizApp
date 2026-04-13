"""
Сервис для определения порядка вопросов в тесте по алгоритму адаптации.
"""

import math
from datetime import datetime
from typing import List
from ..entities.question import Question
from .stats_manager import StatisticsManager
from config import config


class QuizScheduler:
    """
    Сервис, определяющий, в каком порядке (и какие) вопросы должны быть представлены пользователю.
    """

    def __init__(self, stats_manager: StatisticsManager):
        """
        Инициализирует планировщик с менеджером статистики.

        Args:
            stats_manager (StatisticsManager): Экземпляр менеджера статистики.
        """
        self.stats_manager = stats_manager

    def _calculate_priority(self, question_stats: dict) -> float:
        """
        Рассчитывает приоритет вопроса на основе его статистики.
        Чем выше приоритет, тем раньше вопрос должен быть показан.
        """
        total = question_stats["total_answers"]
        correct = question_stats["correct_answers"]
        last_time = question_stats["last_answer_time"]

        # --- Формула приоритета ---
        # 1. Плохая статистика (ошибки)
        error_factor = (total - correct + 1)  # +1, чтобы не было 0

        # 2. Интервальное повторение (упрощённо)
        now = datetime.now().timestamp()
        elapsed_days = (now - last_time) / (24 * 3600)  # Переводим секунды в дни

        stability = config.BASE_STABILITY_DAYS * (config.FACTOR_FOR_CORRECT ** correct)
        retrievability = 1 / (1 + elapsed_days / stability)

        # Итоговый приоритет
        priority = error_factor / (retrievability + config.EPSILON)
        return priority

    def get_questions_for_session(self, test_id: str, questions: List[Question], mode: str = "adaptive") -> List[
        Question]:
        """
        Возвращает список вопросов для текущей сессии, отсортированный по приоритету.

        Args:
            test_id (str): ID текущего теста.
            questions (List[Question]): Исходный список вопросов.
            mode (str): Режим выбора ("adaptive", "errors_only").

        Returns:
            List[Question]: Список вопросов для сессии.
        """
        if mode == "errors_only":
            # Фильтруем вопросы, на которые были ошибки
            filtered_questions = [
                q for q in questions
                if self.stats_manager.get_question_stats(test_id, q.id)["total_answers"] > 0
                   and self.stats_manager.get_question_stats(test_id, q.id)["correct_answers"] <
                   self.stats_manager.get_question_stats(test_id, q.id)["total_answers"]
            ]
        else:  # adaptive
            filtered_questions = questions

        # Сортируем по приоритету (от большего к меньшему)
        sorted_questions = sorted(filtered_questions, key=lambda q: self._calculate_priority(
            self.stats_manager.get_question_stats(test_id, q.id)), reverse=True)

        return sorted_questions