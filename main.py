"""
Точка входа в приложение.
Пока просто инициализирует core компоненты для проверки.
"""

from core.services.data_loader import DataLoader
from core.services.stats_manager import StatisticsManager
from core.services.quiz_scheduler import QuizScheduler
from core.utils.helpers import shuffle_options

def main():
    print("--- Запуск приложения тестирования ---")

    # Инициализация сервисов
    stats_manager = StatisticsManager()
    scheduler = QuizScheduler(stats_manager)
    data_loader = DataLoader()

    # Загрузка тестов
    tests = data_loader.load_tests_from_directory()
    print(f"Загружено {len(tests)} тестов.")

    # Пример: Выбираем первый тест для демонстрации
    if tests:
        selected_test = tests[0]
        print(f"\nВыбран тест: {selected_test.title}")

        # Пример перемешивания опций для первого вопроса
        first_q = selected_test.questions[0]
        print(f"\nВопрос: {first_q.text}")
        print(f"Опции до перемешивания: {[opt['text'] for opt in first_q.options]}")
        shuffled_opts = shuffle_options(first_q.options)
        print(f"Опции после перемешивания: {[opt['text'] for opt in shuffled_opts]}")

        # Пример получения вопросов по алгоритму
        session_questions = scheduler.get_questions_for_session(selected_test.id, selected_test.questions, mode="adaptive")
        print(f"\nПорядок вопросов для сессии (режим adaptive): {[q.id for q in session_questions]}")

        session_questions_errors = scheduler.get_questions_for_session(selected_test.id, selected_test.questions, mode="errors_only")
        print(f"Порядок вопросов для сессии (режим errors_only): {[q.id for q in session_questions_errors]}")


if __name__ == "__main__":
    main()