"""
Сущность Теста.
Содержит информацию о тесте и список вопросов.
"""

from typing import List
from .question import Question

class Test:
    """
    Класс, представляющий один тест (например, по одной главе).
    """

    def __init__(self, t_id: str, title: str, questions: List[Question]):
        """
        Инициализирует объект Test.

        Args:
            t_id (str): Уникальный идентификатор теста.
            title (str): Заголовок теста.
            questions (List[Question]): Список вопросов теста.
        """
        self.id = t_id
        self.title = title
        self.questions = questions # Список объектов Question

    @classmethod
    def from_dict(cls, data: dict) -> 'Test':
        """
        Создаёт экземпляр Test из словаря (например, из JSON).
        """
        questions = [Question.from_dict(q_data) for q_data in data.get('questions', [])]
        return cls(t_id=data['id'], title=data.get('title', ''), questions=questions)