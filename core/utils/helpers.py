"""
Вспомогательные утилиты.
"""

import random

def shuffle_options(options: list) -> list:
    """
    Создаёт копию списка опций и перемешивает её.

    Args:
        options (list): Список опций (словарей).

    Returns:
        list: Перемешанная копия списка.
    """
    options_copy = options.copy()
    random.shuffle(options_copy)
    return options_copy