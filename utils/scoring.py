from data.quiz_data import ANIMALS


def calculate_result(scores: dict) -> dict:
    """
    Определяет тотемное животное на основе набранных баллов.
    
    :param scores: Словарь вида {"manul": 5, "elephant": 3, ...}
    :return: Словарь с данными победившего животного
    """
    if not scores:
        # Если баллов нет (пользователь не отвечал), возвращаем манула по умолчанию
        return ANIMALS["manul"]
    
    # Находим животное с максимальным количеством баллов
    winner_id = max(scores, key=scores.get)
    
    return ANIMALS[winner_id]


def get_initial_scores() -> dict:
    """
    Создаёт пустой словарь для подсчёта баллов.
    Каждому животному присваивается 0 баллов.
    """
    return {animal_id: 0 for animal_id in ANIMALS.keys()}