from django import template

register = template.Library()

@register.filter
def default_if_none_or_empty(value, default=''):
    """
    Returns value if it's not None and not empty string, otherwise returns default.
    This is different from the built-in 'default' filter which also replaces 0.
    Preserves numeric zero values.
    """
    if value is None or value == '':
        return default
    # Важно: сохраняем значение 0 (ноль)
    if value == 0 or value == 0.0:
        return value
    return value

@register.filter
def format_float(value):
    """
    Форматирует число с плавающей точкой для использования в HTML input.
    Обрабатывает различные форматы чисел и возвращает строку с точкой.
    """
    if value is None or value == '':
        return ''
    
    # Обрабатываем различные типы данных
    try:
        # Если это уже float или int
        if isinstance(value, (int, float)):
            # Просто преобразуем в строку
            # Python автоматически использует точку как разделитель
            return str(value)
        else:
            # Если это строка, заменяем запятую на точку
            return str(value).replace(',', '.')
    except (ValueError, TypeError):
        return ''
