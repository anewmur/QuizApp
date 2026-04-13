"""
Сервис для загрузки тестов из JSON файлов.
"""

import json
import os
from typing import List
from ..entities.test import Test
from config import config

class DataLoader:
    """
    Сервис, отвечающий за загрузку и предоставление списка тестов.
    """

    def load_tests_from_directory(self) -> List[Test]:
        """
        Сканирует директорию TESTS_DIR и загружает все JSON файлы как объекты Test.

        Returns:
            List[Test]: Список загруженных тестов.
        """
        tests = []
        if not os.path.exists(config.TESTS_DIR):
            print(f"Директория с тестами '{config.TESTS_DIR}' не найдена.")
            return tests

        for filename in os.listdir(config.TESTS_DIR):
            if filename.lower().endswith('.json'):
                filepath = os.path.join(config.TESTS_DIR, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    test = Test.from_dict(data)
                    tests.append(test)
                    print(f"Загружен тест: {test.title} ({test.id})")
                except json.JSONDecodeError as e:
                    print(f"Ошибка при чтении JSON из файла {filepath}: {e}")
                except Exception as e:
                    print(f"Неизвестная ошибка при загрузке файла {filepath}: {e}")
        return tests