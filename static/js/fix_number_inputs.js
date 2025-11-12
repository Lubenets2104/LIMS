// Функция для исправления проблемы с локалью в полях number
function fixNumberInputs() {
    console.log('Fixing number inputs for locale issues...');
    
    // Находим все input поля
    const fields = document.querySelectorAll('input');
    
    fields.forEach(field => {
        // Получаем значение из атрибута value
        const rawValue = field.getAttribute('value');
        
        if (rawValue && rawValue !== '' && !isNaN(rawValue)) {
            // Устанавливаем значение программно
            field.value = rawValue;
            
            // Для отладки
            if (field.id) {
                console.log(`Fixed ${field.id}: ${rawValue}`);
            }
        }
    });
}

// Запускаем исправление при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, fixing inputs...');
    // Небольшая задержка для гарантии загрузки всех элементов
    setTimeout(fixNumberInputs, 100);
    
    // Запускаем еще раз через секунду на всякий случай
    setTimeout(fixNumberInputs, 1000);
});

// Также запускаем сразу при загрузке скрипта
if (document.readyState === 'complete' || document.readyState === 'interactive') {
    fixNumberInputs();
}

// Экспортируем функцию для ручного вызова
window.fixNumberInputs = fixNumberInputs;
