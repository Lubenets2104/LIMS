/**
 * JavaScript для расчетов в листе измерений эмульсии по ГОСТ 58952.1-2020
 */

// Глобальный объект для экспорта функций
window.emulsionCalculations = {};

// === ОСТАТОК НА СИТЕ 0,14 ===
window.emulsionCalculations.calculateRemaining = function() {
    const w1 = parseFloat(document.getElementById('remaining_w1')?.value) || 0;
    const w2 = parseFloat(document.getElementById('remaining_w2')?.value) || 0;
    const w3 = parseFloat(document.getElementById('remaining_w3')?.value) || 0;
    const w4 = parseFloat(document.getElementById('remaining_w4')?.value) || 0;
    const w5 = parseFloat(document.getElementById('remaining_w5')?.value) || 0;
    
    console.log('calculateRemaining вызвана с параметрами:', {w1, w2, w3, w4, w5});
    
    // Проверяем наличие всех значений
    if (w1 >= 0 && w2 >= 0 && w3 >= 0 && w4 >= 0 && w5 >= 0) {
        // Формула: Остаток = (w5 - w1) / (w3 - (w4 - w2)) * 100
        const emulsionMass = w3 - (w4 - w2);
        
        console.log('Расчет остатка на сите:');
        console.log('Масса использованной эмульсии = w3 - (w4 - w2) =', w3, '- (', w4, '-', w2, ') =', emulsionMass);
        
        const field = document.getElementById('remaining_value');
        if (field) {
            if (emulsionMass !== 0) {
                const result = ((w5 - w1) / emulsionMass * 100).toFixed(2);
                console.log('Остаток = (w5 - w1) / emulsionMass * 100 = (', w5, '-', w1, ') /', emulsionMass, '* 100 =', result, '%');
                
                // Проверка на адекватность результата
                if (Math.abs(result) > 10000) {
                    console.error('Результат вне разумных пределов:', result);
                    field.value = 'Ошибка данных';
                    field.classList.add('input-alert');
                } else {
                    field.value = result;
                    // Подсветка при некорректных данных
                    if (emulsionMass < 0) {
                        field.classList.add('input-alert');
                    } else {
                        field.classList.remove('input-alert');
                    }
                }
            } else {
                console.warn('Деление на ноль! Масса использованной эмульсии = 0');
                field.value = 'Деление на 0';
                field.classList.add('input-alert');
            }
            
            // Предупреждение о некорректных данных
            if (emulsionMass < 0) {
                console.error('ВНИМАНИЕ: Масса использованной эмульсии отрицательная!');
                console.error('Проверьте корректность данных: масса стакана с остатком не должна превышать сумму массы стакана и эмульсии');
            }
        }
    }
};

// === ОСТАТОК НА СИТЕ 0,14 ПОСЛЕ 7 СУТОК ===
window.emulsionCalculations.calculateRemainingAfter7 = function() {
    const w1 = parseFloat(document.getElementById('remaining_after7_w1')?.value) || 0;
    const w2 = parseFloat(document.getElementById('remaining_after7_w2')?.value) || 0;
    const w3 = parseFloat(document.getElementById('remaining_after7_w3')?.value) || 0;
    const w4 = parseFloat(document.getElementById('remaining_after7_w4')?.value) || 0;
    const w5 = parseFloat(document.getElementById('remaining_after7_w5')?.value) || 0;
    
    if (w1 >= 0 && w2 >= 0 && w3 >= 0 && w4 >= 0 && w5 >= 0) {
        const emulsionMass = w3 - (w4 - w2);
        
        const field = document.getElementById('remaining_after7_value');
        if (field) {
            if (emulsionMass !== 0) {
                const result = ((w5 - w1) / emulsionMass * 100).toFixed(2);
                field.value = result;
                
                if (Math.abs(result) > 10000) {
                    field.value = 'Ошибка данных';
                    field.classList.add('input-alert');
                } else if (emulsionMass < 0) {
                    field.classList.add('input-alert');
                } else {
                    field.classList.remove('input-alert');
                }
            } else {
                field.value = 'Деление на 0';
                field.classList.add('input-alert');
            }
        }
    }
};

// === ИНДЕКС РАСПАДА ===
window.emulsionCalculations.calculateDecayIndex = function() {
    const w1 = parseFloat(document.getElementById('decay_index_w1')?.value) || 0;
    const w2 = parseFloat(document.getElementById('decay_index_w2')?.value) || 0;
    const w3 = parseFloat(document.getElementById('decay_index_w3')?.value) || 0;
    
    if (w1 >= 0 && w2 > 0 && w3 > 0) {
        const denominator = w2 - w1;
        if (denominator !== 0) {
            const result = ((w3 - w2) / denominator * 100).toFixed(1);
            
            const field = document.getElementById('decay_index_value');
            if (field) {
                field.value = result;
            }
        }
    }
};

// === СОДЕРЖАНИЕ ВЯЖУЩЕГО С ЭМУЛЬГАТОРОМ ===
window.emulsionCalculations.calculateBinderContent = function() {
    const w1 = parseFloat(document.getElementById('binder_content_w1')?.value) || 0;
    const w2 = parseFloat(document.getElementById('binder_content_w2')?.value) || 0;
    const w3 = parseFloat(document.getElementById('binder_content_w3')?.value) || 0;
    
    if (w1 >= 0 && w2 > 0 && w3 >= 0) {
        const result = ((w3 - w1) / w2 * 100).toFixed(1);
        
        const field = document.getElementById('binder_content_value');
        if (field) {
            field.value = result;
            
            // Рассчитываем массу для минерального материала
            if (result > 0) {
                const mineralMass = (10 / result * 100).toFixed(1);
                const mineralField = document.getElementById('mineral_material_adhesion');
                if (mineralField) {
                    mineralField.value = mineralMass;
                }
            }
        }
    }
};

// === УСТОЙЧИВОСТЬ К РАССЛОЕНИЮ ===
window.emulsionCalculations.calculateDelamination = function(cylinderNum) {
    const volume = parseFloat(document.getElementById(`resistance_cylinder${cylinderNum}_volume`)?.value) || 0;
    const volumeAfter7 = parseFloat(document.getElementById(`resistance_cylinder${cylinderNum}_volume_after7`)?.value) || 0;
    
    console.log(`calculateDelamination для цилиндра ${cylinderNum}:`, {volume, volumeAfter7});
    
    if (volume > 0 && volumeAfter7 >= 0) {
        // Формула: Расслоение = (volume - volumeAfter7) / (7 * volume) * 100
        const result = ((volume - volumeAfter7) / (7 * volume) * 100).toFixed(2);
        
        const field = document.getElementById(`resistance_cylinder${cylinderNum}_delamination`);
        if (field) {
            field.value = result;
            console.log(`Расслоение цилиндра ${cylinderNum} = ${result}%`);
        }
        
        // Вызываем расчет среднего
        window.emulsionCalculations.calculateResistanceAfter7();
    }
};

window.emulsionCalculations.calculateResistanceAfter7 = function() {
    const delamination1 = parseFloat(document.getElementById('resistance_cylinder1_delamination')?.value) || 0;
    const delamination2 = parseFloat(document.getElementById('resistance_cylinder2_delamination')?.value) || 0;
    
    console.log('calculateResistanceAfter7:', {delamination1, delamination2});
    
    if (delamination1 !== 0 || delamination2 !== 0) {
        let result;
        if (delamination1 !== 0 && delamination2 !== 0) {
            // Оба значения есть - считаем среднее
            result = ((delamination1 + delamination2) / 2).toFixed(2);
        } else if (delamination1 !== 0) {
            // Только первое значение
            result = delamination1.toFixed(2);
        } else {
            // Только второе значение
            result = delamination2.toFixed(2);
        }
        
        const field = document.getElementById('resistance_after7_value');
        if (field) {
            field.value = result;
            console.log(`Устойчивость к расслоению (среднее) = ${result}%`);
        }
    }
};

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('Инициализация расчетов для эмульсии ГОСТ 58952.1-2020');
    console.log('window.emulsionCalculations доступен:', window.emulsionCalculations);
    
    // Привязка обработчиков событий для остатка на сите
    ['remaining_w1', 'remaining_w2', 'remaining_w3', 'remaining_w4', 'remaining_w5'].forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', window.emulsionCalculations.calculateRemaining);
            element.addEventListener('change', window.emulsionCalculations.calculateRemaining);
        }
    });
    
    // Привязка обработчиков событий для остатка на сите после 7 суток
    ['remaining_after7_w1', 'remaining_after7_w2', 'remaining_after7_w3', 'remaining_after7_w4', 'remaining_after7_w5'].forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', window.emulsionCalculations.calculateRemainingAfter7);
            element.addEventListener('change', window.emulsionCalculations.calculateRemainingAfter7);
        }
    });
    
    // Индекс распада
    ['decay_index_w1', 'decay_index_w2', 'decay_index_w3'].forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', window.emulsionCalculations.calculateDecayIndex);
            element.addEventListener('change', window.emulsionCalculations.calculateDecayIndex);
        }
    });
    
    // Содержание вяжущего
    ['binder_content_w1', 'binder_content_w2', 'binder_content_w3'].forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', window.emulsionCalculations.calculateBinderContent);
            element.addEventListener('change', window.emulsionCalculations.calculateBinderContent);
        }
    });
    
    // Устойчивость к расслоению - цилиндр 1
    ['resistance_cylinder1_volume', 'resistance_cylinder1_volume_after7'].forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', () => window.emulsionCalculations.calculateDelamination(1));
            element.addEventListener('change', () => window.emulsionCalculations.calculateDelamination(1));
        }
    });
    
    // Устойчивость к расслоению - цилиндр 2
    ['resistance_cylinder2_volume', 'resistance_cylinder2_volume_after7'].forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', () => window.emulsionCalculations.calculateDelamination(2));
            element.addEventListener('change', () => window.emulsionCalculations.calculateDelamination(2));
        }
    });
    
    // Выполняем начальные расчеты
    setTimeout(function() {
        console.log('Выполняем начальные расчеты...');
        window.emulsionCalculations.calculateDecayIndex();
        window.emulsionCalculations.calculateBinderContent();
        window.emulsionCalculations.calculateRemaining();
        window.emulsionCalculations.calculateRemainingAfter7();
        window.emulsionCalculations.calculateDelamination(1);
        window.emulsionCalculations.calculateDelamination(2);
    }, 100);
    
    console.log('Скрипт расчетов для эмульсии ГОСТ 58952.1-2020 загружен и готов к работе');
});
