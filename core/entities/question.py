"""
Сущность Вопроса.
Содержит текст, варианты, правильные ответы, объяснение и теги.
"""

from typing import List, Dict, Any

class Question:
    """
    Класс, представляющий один вопрос теста.
    """

    def __init__(self, q_id: str, text: str, options: List[Dict[str, str]], correct_ids: List[str], explanation: str, tags: List[str]):
        """
        Инициализирует объект Question.

        Args:
            q_id (str): Уникальный идентификатор вопроса.
            text (str): Текст вопроса.
            options (List[Dict[str, str]]): Список словарей с ключами 'id' и 'text'.
            correct_ids (List[str]): Список идентификаторов правильных вариантов.
            explanation (str): Объяснение к вопросу.
            tags (List[str]): Список тегов вопроса.
        """
        self.id = q_id
        self.text = text
        self.options = options
        self.correct_option_ids = set(correct_ids) # Используем set для быстрой проверки
        self.explanation = explanation
        self.tags = tags
        # Состояние для текущего сеанса (перемешанные опции)
        self._shuffled_options = None

    def get_shuffled_options(self) -> List[Dict[str, str]]:
        """
        Возвращает перемешанный список опций.
        Если ещё не перемешивался, возвращает оригинальный список.
        """
        return self._shuffled_options if self._shuffled_options else self.options

    def set_shuffled_options(self, shuffled_list: List[Dict[str, str]]):
        """
        Устанавливает перемешанный список опций.
        """
        self._shuffled_options = shuffled_list

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Question':
        """
        Создаёт экземпляр Question из словаря (например, из JSON).
        """
        return cls(
            q_id=data['id'],
            text=data['question_text'],
            options=data['options'],
            correct_ids=data.get('correct_option_ids', []), # Поддержка нового формата
            explanation=data.get('explanation', ''),
            tags=data.get('tags', [])
        )