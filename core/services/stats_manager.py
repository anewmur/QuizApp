"""
Сервис для управления статистикой прохождения тестов.
Хранит и загружает данные в JSON файл.
"""

import json
import time
from datetime import datetime
from typing import Dict, Optional
from config import config

class StatisticsManager:
    """
    Сервис, отвечающий за хранение и обновление статистики по тестам и вопросам.
    """

    def __init__(self):
        """
        Инициализирует менеджер, загружая существующую статистику из файла.
        """
        self.stats_file_path = config.STATS_FILE_PATH
        self.data = self._load_statistics()

    def _load_statistics(self) -> Dict:
        """
        Загружает статистику из JSON файла.

        Returns:
            Dict: Словарь статистики.
        """
        try:
            with open(self.stats_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Файл статистики {self.stats_file_path} не найден, создаём пустой.")
            return {"test_results": {}}
        except json.JSONDecodeError as e:
            print(f"Ошибка при чтении JSON статистики: {e}. Используем пустой словарь.")
            return {"test_results": {}}

    def save_statistics(self):
        """
        Сохраняет текущую статистику в JSON файл.
        """
        try:
            with open(self.stats_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении статистики: {e}")

    def get_question_stats(self, test_id: str, question_id: str) -> Dict:
        """
        Получает статистику для конкретного вопроса в тесте.
        Если статистика отсутствует, возвращает стандартный словарь.

        Args:
            test_id (str): ID теста.
            question_id (str): ID вопроса.

        Returns:
            Dict: Словарь статистики вопроса.
        """
        return self.data \
                   .setdefault("test_results", {}) \
                   .setdefault(test_id, {}) \
                   .setdefault("questions_stats", {}) \
                   .setdefault(question_id, {
                       "total_answers": 0,
                       "correct_answers": 0,
                       "last_answer_time": 0,
                       "last_was_correct": False
                   })

    def update_question_stats(self, test_id: str, question_id: str, is_correct: bool):
        """
        Обновляет статистику после ответа на вопрос.

        Args:
            test_id (str): ID теста.
            question_id (str): ID вопроса.
            is_correct (bool): Был ли ответ правильным.
        """
        stats = self.get_question_stats(test_id, question_id)
        stats["total_answers"] += 1
        if is_correct:
            stats["correct_answers"] += 1
        stats["last_answer_time"] = int(time.time()) # Unix timestamp
        stats["last_was_correct"] = is_correct
        # Сохраняем после каждого обновления
        self.save_statistics()