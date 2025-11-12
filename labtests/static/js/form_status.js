/**
 * Проверка статуса формы и автоматическое определение заполненности
 * Используется для всех форм листов измерений
 */

// Функция для определения статуса формы по заполненности полей
function checkFormCompleteness() {
    const form = document.querySelector('form');
    if (!form) return 'draft';
    
    // Получаем все поля ввода в форме (кроме readonly и скрытых)
    const inputs = form.querySelectorAll('input:not([readonly]):not([type="hidden"]), select');
    const totalFields = inputs.length;
    let filledFields = 0;
    let requiredEmpty = false;
    
    inputs.forEach(input => {
        // Проверяем заполненность поля
        if (input.value && input.value.trim() !== '') {
            filledFields++;
        }
        
        // Проверяем обязательные поля (помечены required или имеют определенные имена)
        const isRequired = input.hasAttribute('required') || 
                          input.name.includes('type') || 
                          input.name.includes('mix_name') ||
                          input.name.includes('max_density');
        
        if (isRequired && (!input.value || input.value.trim() === '')) {
            requiredEmpty = true;
        }
    });
    
    // Рассчитываем процент заполненности
    const completenessPercent = totalFields > 0 ? (filledFields / totalFields) * 100 : 0;
    
    // Определяем статус
    let status = 'draft';
    if (requiredEmpty) {
        status = 'in_progress';
    } else if (completenessPercent >= 80) {
        status = 'completed';
    } else if (completenessPercent >= 30) {
        status = 'in_progress';
    }
    
    return {
        status: status,
        percent: Math.round(completenessPercent),
        filled: filledFields,
        total: totalFields,
        requiredEmpty: requiredEmpty
    };
}

// Функция для обновления визуального индикатора статуса
function updateStatusIndicator() {
    const completeness = checkFormCompleteness();
    
    // Создаем или обновляем индикатор статуса
    let indicator = document.getElementById('status-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'status-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            z-index: 1000;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        `;
        document.body.appendChild(indicator);
    }
    
    // Обновляем содержимое и стиль индикатора
    let statusText = '';
    let backgroundColor = '';
    
    switch(completeness.status) {
        case 'completed':
            statusText = `✓ Завершено (${completeness.percent}%)`;
            backgroundColor = '#28a745';
            break;
        case 'in_progress':
            statusText = `⚠ В работе (${completeness.percent}%)`;
            backgroundColor = '#ffc107';
            break;
        default:
            statusText = `📝 Черновик (${completeness.percent}%)`;
            backgroundColor = '#6c757d';
    }
    
    indicator.textContent = statusText;
    indicator.style.backgroundColor = backgroundColor;
    indicator.style.color = 'white';
    
    // Добавляем подсказку при наведении
    indicator.title = `Заполнено ${completeness.filled} из ${completeness.total} полей`;
    
    return completeness;
}

// Функция для проверки обязательных полей перед сохранением
function validateRequiredFields() {
    const form = document.querySelector('form');
    if (!form) return true;
    
    let isValid = true;
    const requiredFields = [];
    
    // Определяем обязательные поля в зависимости от типа формы
    const formId = form.id;
    
    if (formId === 'core-form') {
        // Для кернов
        requiredFields.push(
            'layer1_type',
            'layer1_mix_name',
            'layer1_sample1_g',
            'layer1_sample1_g1',
            'layer1_sample1_g2',
            'layer1_max_density'
        );
    } else if (formId === 'asphalt-form') {
        // Для асфальтобетона
        requiredFields.push(
            'density_1_air',
            'density_1_water',
            'density_1_air_after_water'
        );
    } else if (formId === 'sand-form') {
        // Для песка
        requiredFields.push(
            'grain_initial_weight',
            'dust_initial_weight',
            'dust_after_weight'
        );
    }
    
    // Проверяем каждое обязательное поле
    requiredFields.forEach(fieldName => {
        const field = form.querySelector(`[name="${fieldName}"]`);
        if (field && (!field.value || field.value.trim() === '')) {
            isValid = false;
            // Подсвечиваем пустое обязательное поле
            field.style.borderColor = '#ff0000';
            field.style.borderWidth = '2px';
        } else if (field) {
            // Убираем подсветку если поле заполнено
            field.style.borderColor = '#ddd';
            field.style.borderWidth = '1px';
        }
    });
    
    return isValid;
}

// Функция для автосохранения статуса
function autoSaveStatus() {
    const completeness = checkFormCompleteness();
    const sampleId = window.location.pathname.match(/\/samples\/(\d+)\//)?.[1];
    
    if (sampleId && completeness.status) {
        // Отправляем статус на сервер
        fetch(`/samples/${sampleId}/update-status/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                status: completeness.status
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Статус обновлен:', data);
        })
        .catch(error => {
            console.error('Ошибка обновления статуса:', error);
        });
    }
}

// Вспомогательная функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Обновляем индикатор статуса при загрузке
    updateStatusIndicator();
    
    // Добавляем слушатели на все поля формы
    const form = document.querySelector('form');
    if (form) {
        // Обновляем статус при изменении любого поля
        form.addEventListener('input', function() {
            updateStatusIndicator();
        });
        
        form.addEventListener('change', function() {
            updateStatusIndicator();
        });
        
        // Проверяем обязательные поля перед отправкой
        form.addEventListener('submit', function(e) {
            const completeness = checkFormCompleteness();
            
            // Если форма заполнена менее чем на 30%, предупреждаем пользователя
            if (completeness.percent < 30) {
                const confirmSave = confirm(`Форма заполнена только на ${completeness.percent}%. Вы уверены, что хотите сохранить?`);
                if (!confirmSave) {
                    e.preventDefault();
                    return false;
                }
            }
            
            // Проверяем обязательные поля
            if (!validateRequiredFields()) {
                e.preventDefault();
                alert('Пожалуйста, заполните все обязательные поля (они выделены красной рамкой)');
                return false;
            }
        });
    }
    
    // Автосохранение статуса каждые 30 секунд
    setInterval(autoSaveStatus, 30000);
});

console.log('form_status.js загружен успешно');
