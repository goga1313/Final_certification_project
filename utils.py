import re

def validate_date(date_str: str) -> str:
    """
    Проверяет, что дата в формате YYYY-MM-DD с помощью регулярного выражения.
    """
    if not isinstance(date_str, str):
        raise ValueError("Дата должна быть строкой")
    
    date_str = date_str.strip()
    if not date_str:
        raise ValueError("Дата не может быть пустой")
    
    # Регулярное выражение: 4 цифры, дефис, 2 цифры, дефис, 2 цифры
    if not re.fullmatch(r"^\d{4}-\d{2}-\d{2}$", date_str):
        raise ValueError("Дата должна быть в формате ГГГГ-ММ-ДД (например, 2025-12-23)")
    
    # Дополнительная проверка: реальная дата (например, не 2025-99-99)
    from datetime import datetime
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Дата некорректна (например, 31 февраля)")
    
    return date_str

def validate_category(category_str: str) -> str:
    """
    Проверяет и очищает категорию.
    Не допускает пустые строки и только пробелы.
    """
    if not isinstance(category_str, str):
        raise ValueError("Категория должна быть строкой")
    
    category_str = category_str.strip()
    if not category_str:
        raise ValueError("Категория не может быть пустой")
    
    # Выбирать данные только из выпадающего окна
    if not (category_str == "АИ-95" or category_str == "АИ-92" or category_str == "ДТ"):
        raise ValueError("Категорию необходимо выбрать из выпадающего окна.")  
    return category_str

def validate_volume(volume_str: str) -> float:
    """
    Проверяет и преобразует строку в число.
    Поддерживает точки и запятые как десятичный разделитель.
    Примеры: "100", "100.50", "100,50" → 100.5
    """
    if not isinstance(volume_str, str):
        raise ValueError("Объём должен быть строкой")
    
    volume_str = volume_str.strip()
    if not volume_str:
        raise ValueError("Необходимо ввести значение")
    
    # Заменяем запятую на точку (для русскоязычных пользователей)
    volume_str = volume_str.replace(',', '.')
    
    # Регулярное выражение: число, возможно с десятичной частью
    if not re.fullmatch(r"^\d+(\.\d+)?$", volume_str):
        raise ValueError("Неверный формат ввода объёма. Используйте цифры и, при необходимости, точку или запятую.")
    
    volume = float(volume_str)
    if volume <= 0:
        raise ValueError("Объём должен быть больше нуля")
    return volume

