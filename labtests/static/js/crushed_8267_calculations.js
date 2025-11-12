/**
 * JavaScript для расчетов в листе измерений щебня по ГОСТ 8267-93
 * Универсальная версия с полями partition
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Инициализация расчетов для щебня 8267');
    
    // === СОДЕРЖАНИЕ ПЫЛЕВИДНЫХ И ГЛИНИСТЫХ ЧАСТИЦ ===
    function calculateDustContent() {
        const initialWeight = parseFloat(document.getElementById('dust_initial_weight')?.value) || 0;
        const afterWeight = parseFloat(document.getElementById('dust_after_weight')?.value) || 0;
        
        if (initialWeight > 0) {
            const content = ((initialWeight - afterWeight) / initialWeight * 100).toFixed(1);
            const contentField = document.getElementById('dust_content');
            if (contentField) {
                contentField.value = content;
            }
        }
    }
    
    // Обработчики для пылевидных частиц
    const dustInitial = document.getElementById('dust_initial_weight');
    const dustAfter = document.getElementById('dust_after_weight');
    
    if (dustInitial) {
        dustInitial.addEventListener('input', calculateDustContent);
        dustInitial.addEventListener('change', calculateDustContent);
    }
    if (dustAfter) {
        dustAfter.addEventListener('input', calculateDustContent);
        dustAfter.addEventListener('change', calculateDustContent);
    }
    
    // === ГРАНУЛОМЕТРИЧЕСКИЙ СОСТАВ ===
    function calculateGrainComposition() {
        const totalWeight = parseFloat(document.getElementById('grain_compound_weight')?.value) || 0;
        
        if (totalWeight <= 0) {
            // Очищаем поля если нет общей массы
            for (let i = 0; i < 5; i++) {
                const partialField = document.getElementById(`partition_${i}_partial`);
                const passesField = document.getElementById(`partition_${i}_passes`);
                if (partialField) partialField.value = '';
                if (passesField) passesField.value = '';
            }
            return;
        }
        
        let cumulativePasses = 0;
        
        // Рассчитываем для 5 партиций
        for (let i = 0; i < 5; i++) {
            const weightField = document.getElementById(`partition_${i}_weight`);
            const partialField = document.getElementById(`partition_${i}_partial`);
            const passesField = document.getElementById(`partition_${i}_passes`);
            
            if (weightField && partialField && passesField) {
                const weight = parseFloat(weightField.value) || 0;
                
                // Частный остаток (процент от общей массы)
                const partial = weight > 0 ? (weight / totalWeight * 100).toFixed(1) : '0.0';
                partialField.value = partial;
                
                // Проходы через сито (накопительная сумма частных остатков)
                cumulativePasses += parseFloat(partial);
                passesField.value = cumulativePasses.toFixed(1);
            }
        }
    }
    
    // Обработчики для гранулометрического состава
    const grainWeight = document.getElementById('grain_compound_weight');
    if (grainWeight) {
        grainWeight.addEventListener('input', calculateGrainComposition);
        grainWeight.addEventListener('change', calculateGrainComposition);
    }
    
    for (let i = 0; i < 5; i++) {
        const partitionWeight = document.getElementById(`partition_${i}_weight`);
        if (partitionWeight) {
            partitionWeight.addEventListener('input', calculateGrainComposition);
            partitionWeight.addEventListener('change', calculateGrainComposition);
        }
    }
    
    // === ЛЕЩАДНОСТЬ ===
    function calculateFlakiness() {
        const weight = parseFloat(document.getElementById('flakiness_weight')?.value) || 0;
        const flakyWeight = parseFloat(document.getElementById('flakiness_flaky_weight')?.value) || 0;
        
        if (weight > 0) {
            const flakiness = (flakyWeight / weight * 100).toFixed(2);
            const flakinessField = document.getElementById('flakiness_value');
            if (flakinessField) {
                flakinessField.value = flakiness;
            }
            
            // Определение группы по лещадности согласно ГОСТ 8267-93
            const markField = document.getElementById('flakiness_mark_type');
            if (markField) {
                let group = '';
                const value = parseFloat(flakiness);
                
                if (value <= 10) {
                    group = 'I';  // Кубовидная
                } else if (value <= 15) {
                    group = 'II'; // Улучшенная
                } else if (value <= 25) {
                    group = 'III'; // Обычная
                } else if (value <= 35) {
                    group = 'IV';
                } else if (value <= 50) {
                    group = 'V';
                } else {
                    group = 'Не соотв.';
                }
                
                markField.value = group;
            }
        } else {
            // Очищаем поля если нет массы
            const flakinessField = document.getElementById('flakiness_value');
            const markField = document.getElementById('flakiness_mark_type');
            if (flakinessField) flakinessField.value = '';
            if (markField) markField.value = '';
        }
    }
    
    // Обработчики для лещадности
    const flakinessWeight = document.getElementById('flakiness_weight');
    const flakinessFlaky = document.getElementById('flakiness_flaky_weight');
    
    if (flakinessWeight) {
        flakinessWeight.addEventListener('input', calculateFlakiness);
        flakinessWeight.addEventListener('change', calculateFlakiness);
    }
    if (flakinessFlaky) {
        flakinessFlaky.addEventListener('input', calculateFlakiness);
        flakinessFlaky.addEventListener('change', calculateFlakiness);
    }
    
    // === ДРОБИМОСТЬ ===
    function calculateCrushability() {
        const weight = parseFloat(document.getElementById('crushability_weight')?.value) || 0;
        const afterWeight = parseFloat(document.getElementById('crushability_after_weight')?.value) || 0;
        const type = parseInt(document.getElementById('crushability_type')?.value) || 0;
        
        if (weight > 0) {
            // Дробимость = (масса пробы - масса после) / масса пробы * 100
            const crushability = ((weight - afterWeight) / weight * 100).toFixed(2);
            const crushabilityField = document.getElementById('crushability_value');
            if (crushabilityField) {
                crushabilityField.value = crushability;
            }
            
            // Определение марки по дробимости согласно ГОСТ 8267-93
            const markField = document.getElementById('crushability_mark_type');
            if (markField) {
                let mark = '';
                const value = parseFloat(crushability);
                
                if (type === 0) { // Изверженные и метаморфические породы
                    if (value <= 12) mark = '1400';
                    else if (value <= 16) mark = '1200';
                    else if (value <= 20) mark = '1000';
                    else if (value <= 25) mark = '800';
                    else if (value <= 34) mark = '600';
                    else if (value <= 42) mark = '400';
                    else if (value <= 50) mark = '300';
                    else mark = '200';
                } else if (type === 1) { // Осадочные породы
                    if (value <= 10) mark = '1200';
                    else if (value <= 14) mark = '1000';
                    else if (value <= 18) mark = '800';
                    else if (value <= 26) mark = '600';
                    else if (value <= 34) mark = '400';
                    else if (value <= 42) mark = '300';
                    else mark = '200';
                }
                
                markField.value = mark;
            }
        } else {
            // Очищаем поля если нет массы
            const crushabilityField = document.getElementById('crushability_value');
            const markField = document.getElementById('crushability_mark_type');
            if (crushabilityField) crushabilityField.value = '';
            if (markField) markField.value = '';
        }
    }
    
    // Обработчики для дробимости
    const crushWeight = document.getElementById('crushability_weight');
    const crushAfter = document.getElementById('crushability_after_weight');
    const crushType = document.getElementById('crushability_type');
    
    if (crushWeight) {
        crushWeight.addEventListener('input', calculateCrushability);
        crushWeight.addEventListener('change', calculateCrushability);
    }
    if (crushAfter) {
        crushAfter.addEventListener('input', calculateCrushability);
        crushAfter.addEventListener('change', calculateCrushability);
    }
    if (crushType) {
        crushType.addEventListener('change', calculateCrushability);
    }
    
    // === СОДЕРЖАНИЕ ГЛИНЫ В КОМКАХ ===
    function calculateClayContent() {
        const initialWeight = parseFloat(document.getElementById('clay_initial_weight')?.value) || 0;
        const clayWeight = parseFloat(document.getElementById('clay_weight')?.value) || 0;
        
        if (initialWeight > 0) {
            // Содержание глины = масса глины / масса пробы * 100
            const content = (clayWeight / initialWeight * 100).toFixed(2);
            const contentField = document.getElementById('clay_content');
            if (contentField) {
                contentField.value = content;
            }
        } else {
            const contentField = document.getElementById('clay_content');
            if (contentField) contentField.value = '';
        }
    }
    
    // Обработчики для глины в комках
    const clayInitial = document.getElementById('clay_initial_weight');
    const clayWeight = document.getElementById('clay_weight');
    
    if (clayInitial) {
        clayInitial.addEventListener('input', calculateClayContent);
        clayInitial.addEventListener('change', calculateClayContent);
    }
    if (clayWeight) {
        clayWeight.addEventListener('input', calculateClayContent);
        clayWeight.addEventListener('change', calculateClayContent);
    }
    
    // === ФУНКЦИЯ ОКРУГЛЕНИЯ ===
    function roundValue(value, decimals = 1) {
        return Math.round(value * Math.pow(10, decimals)) / Math.pow(10, decimals);
    }
    
    // === ВАЛИДАЦИЯ ПОЛЕЙ ===
    function validateNumericInput(event) {
        const input = event.target;
        let value = input.value;
        
        // Разрешаем только числа и одну точку
        value = value.replace(/[^0-9.]/g, '');
        
        // Убираем лишние точки
        const parts = value.split('.');
        if (parts.length > 2) {
            value = parts[0] + '.' + parts.slice(1).join('');
        }
        
        input.value = value;
    }
    
    // Добавляем валидацию на все числовые поля
    document.querySelectorAll('input[type="number"]').forEach(input => {
        input.addEventListener('input', validateNumericInput);
    });
    
    // === АВТОСОХРАНЕНИЕ ===
    let saveTimeout;
    function autoSave() {
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => {
            console.log('Автосохранение данных...');
            // Здесь можно добавить AJAX запрос для автосохранения
        }, 2000); // Сохраняем через 2 секунды после последнего изменения
    }
    
    // Добавляем автосохранение на все поля
    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', autoSave);
    });
    
    // === ИНДИКАТОР ЗАПОЛНЕННОСТИ ФОРМЫ ===
    function updateFormCompleteness() {
        const requiredFields = [
            'grain_compound_weight',
            'partition_0_weight', 'partition_1_weight', 'partition_2_weight',
            'dust_initial_weight', 'dust_after_weight',
            'flakiness_weight', 'flakiness_flaky_weight',
            'crushability_weight', 'crushability_after_weight',
            'clay_initial_weight', 'clay_weight'
        ];
        
        let filledCount = 0;
        
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field && field.value && parseFloat(field.value) > 0) {
                filledCount++;
            }
        });
        
        const percentage = Math.round((filledCount / requiredFields.length) * 100);
        console.log(`Форма заполнена на ${percentage}%`);
        
        // Можно добавить визуальный индикатор
        const statusBar = document.querySelector('.form-status');
        if (statusBar) {
            statusBar.style.width = percentage + '%';
            statusBar.textContent = percentage + '%';
        }
    }
    
    // Обновляем статус при изменении полей
    document.querySelectorAll('input[type="number"]').forEach(input => {
        input.addEventListener('input', updateFormCompleteness);
    });
    
    // === ИНИЦИАЛИЗАЦИЯ ПРИ ЗАГРУЗКЕ ===
    // Выполняем все расчеты при загрузке страницы
    setTimeout(() => {
        calculateDustContent();
        calculateGrainComposition();
        calculateFlakiness();
        calculateCrushability();
        calculateClayContent();
        updateFormCompleteness();
        console.log('Все расчеты выполнены при загрузке');
    }, 100);
    
    // === ОБРАБОТКА ОТПРАВКИ ФОРМЫ ===
    const form = document.getElementById('crushed-8267-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Проверяем обязательные поля перед отправкой
            const requiredFields = ['grain_compound_weight'];
            let isValid = true;
            
            requiredFields.forEach(fieldId => {
                const field = document.getElementById(fieldId);
                if (!field || !field.value || parseFloat(field.value) <= 0) {
                    isValid = false;
                    if (field) {
                        field.style.borderColor = 'red';
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Пожалуйста, заполните обязательные поля (масса пробы для гранулометрического состава)');
                return false;
            }
            
            console.log('Форма отправлена');
        });
    }
    
    console.log('Скрипт расчетов для щебня ГОСТ 8267-93 загружен и инициализирован');
});
