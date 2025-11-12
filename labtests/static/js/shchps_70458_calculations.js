// Автоматические расчеты для щебня по ГОСТ 70458-2022

document.addEventListener('DOMContentLoaded', function() {
    console.log('Загружен скрипт расчетов для ГОСТ 70458-2022');
    
    // ========================================
    // СОДЕРЖАНИЕ ПЫЛЕВИДНЫХ И ГЛИНИСТЫХ ЧАСТИЦ
    // ========================================
    
    function calculateDustClay() {
        const initialWeight = parseFloat(document.getElementById('dust_initial_weight').value) || 0;
        const afterWeight = parseFloat(document.getElementById('dust_after_weight').value) || 0;
        
        if (initialWeight > 0 && afterWeight >= 0) {
            const content = ((initialWeight - afterWeight) / initialWeight) * 100;
            document.getElementById('dust_clay_content').value = content.toFixed(1);
        } else {
            document.getElementById('dust_clay_content').value = '';
        }
    }
    
    // Слушатели для пылевидных и глинистых частиц
    document.getElementById('dust_initial_weight').addEventListener('input', calculateDustClay);
    document.getElementById('dust_after_weight').addEventListener('input', calculateDustClay);
    
    // ========================================
    // ГРАНУЛОМЕТРИЧЕСКИЙ СОСТАВ
    // ========================================
    
    const sieves = ['22_4', '16', '11_2', '8', '5_6', '4', '2', '1', '0_5'];
    
    function calculateGrainComposition() {
        const compoundWeight = parseFloat(document.getElementById('grain_compound_weight').value) || 0;
        
        if (compoundWeight <= 0) {
            // Очищаем все расчетные поля если нет массы пробы
            sieves.forEach(sieve => {
                document.getElementById(`sieve_${sieve}_partial`).value = '';
                document.getElementById(`sieve_${sieve}_full`).value = '';
            });
            return;
        }
        
        let cumulativePass = 100; // Начинаем со 100% прохода
        
        sieves.forEach((sieve, index) => {
            const weight = parseFloat(document.getElementById(`sieve_${sieve}_weight`).value) || 0;
            
            // Частный остаток (процент от общей массы)
            const partial = (weight / compoundWeight) * 100;
            document.getElementById(`sieve_${sieve}_partial`).value = partial > 0 ? partial.toFixed(1) : '';
            
            // Проход через сито (накопительный)
            cumulativePass -= partial;
            document.getElementById(`sieve_${sieve}_full`).value = cumulativePass >= 0 ? cumulativePass.toFixed(1) : '0.0';
        });
        
        // Определение категории и марки
        determineCategoryAndMark();
    }
    
    function determineCategoryAndMark() {
        // Получаем значения проходов через сита
        const passes = {};
        sieves.forEach(sieve => {
            const value = parseFloat(document.getElementById(`sieve_${sieve}_full`).value);
            passes[sieve] = isNaN(value) ? null : value;
        });
        
        // Проверяем соответствие различным категориям
        // Полный набор категорий по ГОСТ 70458-2022
        let category = '';
        
        // К90 М1
        if (passes['22_4'] == 100 &&
            passes['16'] >= 90 && passes['16'] <= 100 &&
            passes['8'] >= 63 && passes['8'] <= 77 &&
            passes['4'] >= 43 && passes['4'] <= 57 &&
            passes['2'] >= 30 && passes['2'] <= 42 &&
            passes['1'] >= 22 && passes['1'] <= 33 &&
            passes['0_5'] >= 15 && passes['0_5'] <= 30) {
            category = 'К90 М1';
        }
        // К90 М2
        else if (passes['22_4'] == 100 &&
                 passes['16'] >= 90 && passes['16'] <= 100 &&
                 passes['8'] >= 63 && passes['8'] <= 77 &&
                 passes['4'] >= 43 && passes['4'] <= 60 &&
                 passes['2'] >= 30 && passes['2'] <= 52 &&
                 passes['1'] >= 23 && passes['1'] <= 40 &&
                 passes['0_5'] >= 14 && passes['0_5'] <= 35) {
            category = 'К90 М2';
        }
        // К90 М3
        else if (passes['22_4'] == 100 &&
                 passes['16'] >= 90 && passes['16'] <= 100 &&
                 passes['8'] >= 54 && passes['8'] <= 72 &&
                 passes['4'] >= 33 && passes['4'] <= 52 &&
                 passes['2'] >= 21 && passes['2'] <= 38 &&
                 passes['1'] >= 14 && passes['1'] <= 27 &&
                 passes['0_5'] >= 9 && passes['0_5'] <= 20) {
            category = 'К90 М3';
        }
        // К85 М1
        else if (passes['22_4'] == 100 &&
                 passes['16'] >= 85 && passes['16'] <= 100 &&
                 passes['8'] >= 63 && passes['8'] <= 77 &&
                 passes['4'] >= 43 && passes['4'] <= 57 &&
                 passes['2'] >= 30 && passes['2'] <= 42 &&
                 passes['1'] >= 22 && passes['1'] <= 33 &&
                 passes['0_5'] >= 15 && passes['0_5'] <= 30) {
            category = 'К85 М1';
        }
        // К85 М2
        else if (passes['22_4'] == 100 &&
                 passes['16'] >= 85 && passes['16'] <= 100 &&
                 passes['8'] >= 63 && passes['8'] <= 77 &&
                 passes['4'] >= 43 && passes['4'] <= 60 &&
                 passes['2'] >= 30 && passes['2'] <= 52 &&
                 passes['1'] >= 23 && passes['1'] <= 40 &&
                 passes['0_5'] >= 14 && passes['0_5'] <= 35) {
            category = 'К85 М2';
        }
        // К85 М3
        else if (passes['22_4'] == 100 &&
                 passes['16'] >= 85 && passes['16'] <= 100 &&
                 passes['8'] >= 54 && passes['8'] <= 72 &&
                 passes['4'] >= 33 && passes['4'] <= 52 &&
                 passes['2'] >= 21 && passes['2'] <= 38 &&
                 passes['1'] >= 14 && passes['1'] <= 27 &&
                 passes['0_5'] >= 9 && passes['0_5'] <= 20) {
            category = 'К85 М3';
        }
        else {
            category = 'Не соответствует';
        }
        
        document.getElementById('category_and_mark').value = category;
    }
    
    // Слушатели для гранулометрического состава
    document.getElementById('grain_compound_weight').addEventListener('input', calculateGrainComposition);
    sieves.forEach(sieve => {
        const element = document.getElementById(`sieve_${sieve}_weight`);
        if (element) {
            element.addEventListener('input', calculateGrainComposition);
        }
    });
    
    // ========================================
    // ЛЕЩАДНОСТЬ
    // ========================================
    
    function calculateFlakiness() {
        let totalInitial = 0;
        let totalFlaky = 0;
        let hasData = false;
        
        // Фракция 4-8
        const initial_4_8 = parseFloat(document.getElementById('flakiness_4_8_initial').value) || 0;
        const flaky_4_8 = parseFloat(document.getElementById('flakiness_4_8_flaky').value) || 0;
        
        if (initial_4_8 > 0) {
            const value_4_8 = (flaky_4_8 / initial_4_8) * 100;
            document.getElementById('flakiness_4_8_value').value = value_4_8.toFixed(2);
            totalInitial += initial_4_8;
            totalFlaky += flaky_4_8;
            hasData = true;
        } else {
            document.getElementById('flakiness_4_8_value').value = '';
        }
        
        // Фракция 8-16
        const initial_8_16 = parseFloat(document.getElementById('flakiness_8_16_initial').value) || 0;
        const flaky_8_16 = parseFloat(document.getElementById('flakiness_8_16_flaky').value) || 0;
        
        if (initial_8_16 > 0) {
            const value_8_16 = (flaky_8_16 / initial_8_16) * 100;
            document.getElementById('flakiness_8_16_value').value = value_8_16.toFixed(2);
            totalInitial += initial_8_16;
            totalFlaky += flaky_8_16;
            hasData = true;
        } else {
            document.getElementById('flakiness_8_16_value').value = '';
        }
        
        // Средняя лещадность (взвешенное среднее)
        if (totalInitial > 0 && hasData) {
            const average = (totalFlaky / totalInitial) * 100;
            // Округляем до 2 знаков после запятой для точности
            document.getElementById('flakiness_average').value = average.toFixed(2);
            
            // Определение марки по лещадности согласно ГОСТ 70458-2022
            let mark = '';
            if (average <= 10) {
                mark = 'Л10';
            } else if (average <= 15) {
                mark = 'Л15';
            } else if (average <= 20) {
                mark = 'Л20';
            } else if (average <= 25) {
                mark = 'Л25';
            } else if (average <= 30) {
                mark = 'Л30';
            } else if (average <= 35) {
                mark = 'Л35';
            } else if (average <= 50) {
                mark = 'Л50 (по согласованию)';
            } else {
                mark = 'Марка не определена';
            }
            document.getElementById('flakiness_mark').value = mark;
        } else {
            document.getElementById('flakiness_average').value = '';
            document.getElementById('flakiness_mark').value = '';
        }
    }
    
    // Слушатели для лещадности
    document.getElementById('flakiness_4_8_initial').addEventListener('input', calculateFlakiness);
    document.getElementById('flakiness_4_8_flaky').addEventListener('input', calculateFlakiness);
    document.getElementById('flakiness_8_16_initial').addEventListener('input', calculateFlakiness);
    document.getElementById('flakiness_8_16_flaky').addEventListener('input', calculateFlakiness);
    
    // ========================================
    // ДРОБИМОСТЬ
    // ========================================
    
    function calculateCrushability() {
        let totalInitial = 0;
        let totalCrushed = 0;
        let hasData = false;
        
        // Фракция 4-8
        const initial_4_8 = parseFloat(document.getElementById('crushability_4_8_initial').value) || 0;
        const after_4_8 = parseFloat(document.getElementById('crushability_4_8_after').value) || 0;
        
        if (initial_4_8 > 0) {
            const value_4_8 = ((initial_4_8 - after_4_8) / initial_4_8) * 100;
            document.getElementById('crushability_4_8_value').value = value_4_8.toFixed(2);
            totalInitial += initial_4_8;
            totalCrushed += (initial_4_8 - after_4_8);
            hasData = true;
        } else {
            document.getElementById('crushability_4_8_value').value = '';
        }
        
        // Фракция 8-16
        const initial_8_16 = parseFloat(document.getElementById('crushability_8_16_initial').value) || 0;
        const after_8_16 = parseFloat(document.getElementById('crushability_8_16_after').value) || 0;
        
        if (initial_8_16 > 0) {
            const value_8_16 = ((initial_8_16 - after_8_16) / initial_8_16) * 100;
            document.getElementById('crushability_8_16_value').value = value_8_16.toFixed(2);
            totalInitial += initial_8_16;
            totalCrushed += (initial_8_16 - after_8_16);
            hasData = true;
        } else {
            document.getElementById('crushability_8_16_value').value = '';
        }
        
        // Средняя дробимость (взвешенное среднее)
        if (totalInitial > 0 && hasData) {
            const average = (totalCrushed / totalInitial) * 100;
            // Округляем до 2 знаков после запятой для точности
            document.getElementById('crushability_average').value = average.toFixed(2);
            
            // Определение марки по дробимости
            const rockType = parseInt(document.getElementById('crushability_type').value) || 0;
            let mark = '';
            
            if (rockType === 0) { // Изверженные и метаморфические
                if (average <= 12) {
                    mark = 'М1400';
                } else if (average <= 16) {
                    mark = 'М1200';
                } else if (average <= 20) {
                    mark = 'М1000';
                } else if (average <= 25) {
                    mark = 'М800';
                } else if (average <= 34) {
                    mark = 'М600';
                } else if (average <= 42) {
                    mark = 'М400';
                } else if (average <= 52) {
                    mark = 'М300';
                } else if (average <= 60) {
                    mark = 'М200';
                } else {
                    mark = 'Марка не определена';
                }
            } else { // Осадочные
                if (average <= 10) {
                    mark = 'М1000';
                } else if (average <= 14) {
                    mark = 'М800';
                } else if (average <= 18) {
                    mark = 'М600';
                } else if (average <= 26) {
                    mark = 'М400';
                } else if (average <= 35) {
                    mark = 'М300';
                } else if (average <= 45) {
                    mark = 'М200';
                } else {
                    mark = 'Марка не определена';
                }
            }
            
            document.getElementById('crushability_mark').value = mark;
        } else {
            document.getElementById('crushability_average').value = '';
            document.getElementById('crushability_mark').value = '';
        }
    }
    
    // Слушатели для дробимости
    document.getElementById('crushability_4_8_initial').addEventListener('input', calculateCrushability);
    document.getElementById('crushability_4_8_after').addEventListener('input', calculateCrushability);
    document.getElementById('crushability_8_16_initial').addEventListener('input', calculateCrushability);
    document.getElementById('crushability_8_16_after').addEventListener('input', calculateCrushability);
    document.getElementById('crushability_type').addEventListener('change', calculateCrushability);
    
    // ========================================
    // НАСЫПНАЯ ПЛОТНОСТЬ
    // ========================================
    
    function calculateBulkDensity() {
        let densities = [];
        
        // Первое измерение
        const volume1 = parseFloat(document.getElementById('bulk_density_1_volume').value) || 0;
        const empty1 = parseFloat(document.getElementById('bulk_density_1_empty').value) || 0;
        const weight1 = parseFloat(document.getElementById('bulk_density_1_weight').value) || 0;
        
        if (volume1 > 0 && weight1 > empty1) {
            const density1 = (weight1 - empty1) / volume1;
            document.getElementById('bulk_density_1_density').value = density1.toFixed(2);
            densities.push(density1);
        } else {
            document.getElementById('bulk_density_1_density').value = '';
        }
        
        // Второе измерение
        const volume2 = parseFloat(document.getElementById('bulk_density_2_volume').value) || 0;
        const empty2 = parseFloat(document.getElementById('bulk_density_2_empty').value) || 0;
        const weight2 = parseFloat(document.getElementById('bulk_density_2_weight').value) || 0;
        
        if (volume2 > 0 && weight2 > empty2) {
            const density2 = (weight2 - empty2) / volume2;
            document.getElementById('bulk_density_2_density').value = density2.toFixed(2);
            densities.push(density2);
        } else {
            document.getElementById('bulk_density_2_density').value = '';
        }
        
        // Средняя плотность
        if (densities.length > 0) {
            const average = densities.reduce((a, b) => a + b, 0) / densities.length;
            document.getElementById('bulk_density_average').value = average.toFixed(2);
        } else {
            document.getElementById('bulk_density_average').value = '';
        }
    }
    
    // Слушатели для насыпной плотности
    document.getElementById('bulk_density_1_volume').addEventListener('input', calculateBulkDensity);
    document.getElementById('bulk_density_1_empty').addEventListener('input', calculateBulkDensity);
    document.getElementById('bulk_density_1_weight').addEventListener('input', calculateBulkDensity);
    document.getElementById('bulk_density_2_volume').addEventListener('input', calculateBulkDensity);
    document.getElementById('bulk_density_2_empty').addEventListener('input', calculateBulkDensity);
    document.getElementById('bulk_density_2_weight').addEventListener('input', calculateBulkDensity);
    
    // ========================================
    // СОДЕРЖАНИЕ ГЛИНЫ В КОМКАХ
    // ========================================
    
    function calculateClay() {
        const initialWeight = parseFloat(document.getElementById('clay_initial_weight').value) || 0;
        const clayWeight = parseFloat(document.getElementById('clay_weight').value) || 0;
        
        if (initialWeight > 0 && clayWeight >= 0) {
            const content = (clayWeight / initialWeight) * 100;
            document.getElementById('clay_content').value = content.toFixed(2);
        } else {
            document.getElementById('clay_content').value = '';
        }
    }
    
    // Слушатели для глины в комках
    document.getElementById('clay_initial_weight').addEventListener('input', calculateClay);
    document.getElementById('clay_weight').addEventListener('input', calculateClay);
    
    // ========================================
    // ВАЛИДАЦИЯ ПОЛЕЙ
    // ========================================
    
    // Функция для подсветки незаполненных обязательных полей
    function validateRequiredFields() {
        const requiredFields = [
            'dust_initial_weight', 'dust_after_weight',
            'grain_compound_weight',
            'sieve_22_4_weight', 'sieve_16_weight', 'sieve_11_2_weight',
            'sieve_8_weight', 'sieve_5_6_weight', 'sieve_4_weight',
            'sieve_2_weight', 'sieve_1_weight', 'sieve_0_5_weight'
        ];
        
        let allFilled = true;
        
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                const value = field.value.trim();
                if (!value || parseFloat(value) === 0) {
                    field.classList.add('input-alert');
                    allFilled = false;
                } else {
                    field.classList.remove('input-alert');
                }
            }
        });
        
        return allFilled;
    }
    
    // Проверка при отправке формы
    document.getElementById('shchps-form').addEventListener('submit', function(e) {
        const isValid = validateRequiredFields();
        if (!isValid) {
            alert('Пожалуйста, заполните все обязательные поля (выделены красным)');
            e.preventDefault();
            return false;
        }
    });
    
    // ========================================
    // ИНИЦИАЛИЗАЦИЯ
    // ========================================
    
    // Запускаем все расчеты при загрузке страницы
    calculateDustClay();
    calculateGrainComposition();
    calculateFlakiness();
    calculateCrushability();
    calculateBulkDensity();
    calculateClay();
    
    console.log('Инициализация расчетов завершена');
});

// Функция для форматирования чисел
function formatNumber(value, decimals = 1) {
    if (value === null || value === undefined || isNaN(value)) {
        return '';
    }
    return parseFloat(value).toFixed(decimals);
}

// Функция для безопасного парсинга чисел
function safeParseFloat(value) {
    const parsed = parseFloat(value);
    return isNaN(parsed) ? 0 : parsed;
}
