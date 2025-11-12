from django import template

register = template.Library()

@register.filter
def floatformat_dot(value):
    """
    Форматирует число с точкой как десятичным разделителем
    для использования в HTML input type="number"
    """
    if value is None or value == '':
        return ''
    try:
        # Преобразуем в float и затем в строку с точкой
        float_value = float(value)
        # Используем стандартное форматирование Python (с точкой)
        return str(float_value)
    except (ValueError, TypeError):
        return ''
