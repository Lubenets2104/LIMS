/**
 * JavaScript для расчетов в листе измерений минерального порошка по ГОСТ 32761-2014
 */

// Глобальный объект для экспорта функций
window.mineralPowderCalculations = {};

// Коэффициент для расчета истинной плотности
const IS_ACTIVE_COEFFICIENT = 0.9;

// === ГРАНУЛОМЕТРИЧЕСКИЙ СОСТАВ ===
window.mineralPowderCalculations.calculateCompounds = function() {
    const sampleWeight = parseFloat(document.getElementById('sample_weight')?.value) || 0;
    
    if (sampleWeight <= 0) return;
    
    const sieves = [
        { id: 'sieve_2_0125', name: '2-0.125' },
        { id: 'sieve_0125', name: '0.125' },
        { id: 'sieve_0063', name: '0.063' },
        { id: 'sieve_less_0063', name: '<0.063' }
    ];
    
    let prevFullRemainder = 0;
    
    sieves.forEach((sieve, index) => {
        const weight = parseFloat(document.getElementById(`${sieve.id}_weight`)?.value) || 0;
        
        if (weight >= 0 && sampleWeight > 0) {
            // Частный остаток = (навеска / масса пробы) * 100
            const remainder = (weight / sampleWeight) * 100;
            
            // Полный остаток = предыдущий полный остаток + частный остаток
            const fullRemainder = prevFullRemainder + remainder;
            
            // Полный проход = 100 - полный остаток
            const passes = 100 - fullRemainder;
            
            // Записываем результаты
            const remainderField = document.getElementById(`${sieve.id}_remainder`);
            if (remainderField) remainderField.value = remainder.toFixed(2);
            
            const fullRemainderField = document.getElementById(`${sieve.id}_full_remainder`);
            if (fullRemainderField) fullRemainderField.value = fullRemainder.toFixed(2);
            
            const passesField = document.getElementById(`${sieve.id}_passes`);
            if (passesField) {
                passesField.value = passes.toFixed(2);
                
                // Валидация для определенных сит
                if (sieve.id === 'sieve_0063' && passes < 70) {
                    passesField.classList.add('input-alert');
                } else {
                    passesField.classList.remove('input-alert');
                }
            }
            
            prevFullRemainder = fullRemainder;
        }
    });
};

// === ВЛАЖНОСТЬ ===
window.mineralPowderCalculations.calculateHumidity = function() {
    const plateBefore = parseFloat(document.getElementById('humidity_plate_weight_before')?.value) || 0;
    const plateAfter = parseFloat(document.getElementById('humidity_plate_weight_after')?.value) || 0;
    const plateWeight = parseFloat(document.getElementById('humidity_plate_weight')?.value) || 0;
    
    if (plateBefore > 0 && plateAfter > 0 && plateWeight > 0) {
        // Формула по ГОСТ 32761-2014 (п. 7.2):
        // W = ((m_влажн - m_сух) / m_сух) × 100%
        // где:
        // m_влажн = масса влажной пробы (без чаши) = plateBefore - plateWeight
        // m_сух = масса сухой пробы (без чаши) = plateAfter - plateWeight
        
        const wetSampleWeight = plateBefore - plateWeight;  // масса влажной пробы
        const drySampleWeight = plateAfter - plateWeight;   // масса сухой пробы
        
        // Проверяем корректность данных
        if (drySampleWeight <= 0) {
            console.error('Ошибка: масса сухой пробы должна быть больше 0');
            const field = document.getElementById('humidity_value');
            if (field) {
                field.value = 'Ошибка';
                field.classList.add('input-alert');
            }
            return;
        }
        
        // Рассчитываем влажность по ГОСТ
        const humidity = ((wetSampleWeight - drySampleWeight) / drySampleWeight) * 100;
        
        const field = document.getElementById('humidity_value');
        if (field) {
            field.value = humidity.toFixed(2);
            
            // Валидация - для минерального порошка влажность должна быть < 1%
            if (humidity > 1) {
                field.classList.add('input-alert');
            } else {
                field.classList.remove('input-alert');
            }
        }
    }
};

// === ИСТИННАЯ ПЛОТНОСТЬ ===
window.mineralPowderCalculations.calculateRealDensity = function(index) {
    const wp = parseFloat(document.getElementById(`real_density_${index}_weight_with_powder`)?.value) || 0;
    const ew = parseFloat(document.getElementById(`real_density_${index}_empty_weight`)?.value) || 0;
    const ww = parseFloat(document.getElementById(`real_density_${index}_weight_with_water`)?.value) || 0;
    const wpw = parseFloat(document.getElementById(`real_density_${index}_weight_with_powder_and_water`)?.value) || 0;
    
    if (wp > 0 && ew > 0 && ww > 0 && wpw > 0) {
        // Плотность = ((wp - ew) * k) / (wp - ew + ww - wpw)
        const density = ((wp - ew) * IS_ACTIVE_COEFFICIENT) / (wp - ew + ww - wpw);
        
        const field = document.getElementById(`real_density_${index}_value`);
        if (field) {
            field.value = density.toFixed(2);
        }
        
        // Пересчитываем среднее
        window.mineralPowderCalculations.calculateAverageRealDensity();
    }
};

window.mineralPowderCalculations.calculateAverageRealDensity = function() {
    const d1 = parseFloat(document.getElementById('real_density_1_value')?.value) || 0;
    const d2 = parseFloat(document.getElementById('real_density_2_value')?.value) || 0;
    
    if (d1 > 0 && d2 > 0) {
        const average = (d1 + d2) / 2;
        
        const field = document.getElementById('real_density_average');
        if (field) {
            field.value = average.toFixed(2);
            
            // Автоматически заполняем плотность для битумоемкости
            const bitumenField = document.getElementById('bitumen_capacity_real_density');
            if (bitumenField && (!bitumenField.value || bitumenField.value == '0')) {
                bitumenField.value = average.toFixed(2);
            }
        }
        
        // Пересчитываем пористость
        window.mineralPowderCalculations.calculatePorosity();
    }
};

// === СРЕДНЯЯ ПЛОТНОСТЬ ===
window.mineralPowderCalculations.calculateAverageDensity = function() {
    const bwp = parseFloat(document.getElementById('average_density_bottom_weight_with_powder')?.value) || 0;
    const bw = parseFloat(document.getElementById('average_density_bottom_weight')?.value) || 0;
    const volume = parseFloat(document.getElementById('average_density_volume')?.value) || 0;
    
    if (bwp > 0 && bw > 0 && volume > 0) {
        // Средняя плотность = (масса с порошком - масса без) / объем
        const density = (bwp - bw) / volume;
        
        const field = document.getElementById('average_density_value');
        if (field) {
            field.value = density.toFixed(2);
        }
        
        // Пересчитываем пористость
        window.mineralPowderCalculations.calculatePorosity();
    }
};

// === ПОРИСТОСТЬ ===
window.mineralPowderCalculations.calculatePorosity = function() {
    const averageDensity = parseFloat(document.getElementById('average_density_value')?.value) || 0;
    const realDensity = parseFloat(document.getElementById('real_density_average')?.value) || 0;
    
    if (averageDensity > 0 && realDensity > 0) {
        // Пористость = (1 - средняя плотность / истинная плотность) * 100
        const porosity = (1 - (averageDensity / realDensity)) * 100;
        
        const field = document.getElementById('porosity');
        if (field) {
            field.value = porosity.toFixed(2);
            
            // Валидация (обычно пористость 30-40%)
            if (porosity < 30 || porosity > 40) {
                field.classList.add('input-alert');
            } else {
                field.classList.remove('input-alert');
            }
        }
    }
};

// === БИТУМОЕМКОСТЬ ===
window.mineralPowderCalculations.calculateBitumenCapacity = function() {
    const weight = parseFloat(document.getElementById('bitumen_capacity_weight')?.value) || 0;
    const weightAfter = parseFloat(document.getElementById('bitumen_capacity_weight_after')?.value) || 0;
    const oilWeight = parseFloat(document.getElementById('bitumen_capacity_oil_weight')?.value) || 0;
    const realDensity = parseFloat(document.getElementById('bitumen_capacity_real_density')?.value) || 0;
    
    if (weight > 0 && weightAfter > 0 && oilWeight > 0 && realDensity > 0 && weight > weightAfter) {
        // Битумоемкость = (масса масла - истинная плотность) / (масса до - масса после)
        const bitumenCapacity = (oilWeight - realDensity) / (weight - weightAfter);
        
        const field = document.getElementById('bitumen_capacity_value');
        if (field) {
            field.value = bitumenCapacity.toFixed(2);
            
            // Валидация
            if (bitumenCapacity < 0) {
                field.classList.add('input-alert');
            } else {
                field.classList.remove('input-alert');
            }
        }
    }
};

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('Инициализация расчетов для минерального порошка ГОСТ 32761-2014');
    
    // === Привязка обработчиков событий ===
    
    // Гранулометрический состав
    const sampleWeight = document.getElementById('sample_weight');
    if (sampleWeight) {
        sampleWeight.addEventListener('input', window.mineralPowderCalculations.calculateCompounds);
        sampleWeight.addEventListener('change', window.mineralPowderCalculations.calculateCompounds);
    }
    
    ['sieve_2_0125', 'sieve_0125', 'sieve_0063', 'sieve_less_0063'].forEach(id => {
        const element = document.getElementById(`${id}_weight`);
        if (element) {
            element.addEventListener('input', window.mineralPowderCalculations.calculateCompounds);
            element.addEventListener('change', window.mineralPowderCalculations.calculateCompounds);
        }
    });
    
    // Влажность
    ['humidity_plate_weight_before', 'humidity_plate_weight_after', 'humidity_plate_weight'].forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', window.mineralPowderCalculations.calculateHumidity);
            element.addEventListener('change', window.mineralPowderCalculations.calculateHumidity);
        }
    });
    
    // Истинная плотность
    for (let i = 1; i <= 2; i++) {
        ['weight_with_powder', 'empty_weight', 'weight_with_water', 'weight_with_powder_and_water'].forEach(param => {
            const element = document.getElementById(`real_density_${i}_${param}`);
            if (element) {
                element.addEventListener('input', () => window.mineralPowderCalculations.calculateRealDensity(i));
                element.addEventListener('change', () => window.mineralPowderCalculations.calculateRealDensity(i));
            }
        });
    }
    
    // Средняя плотность
    ['average_density_bottom_weight_with_powder', 'average_density_bottom_weight', 'average_density_volume'].forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', window.mineralPowderCalculations.calculateAverageDensity);
            element.addEventListener('change', window.mineralPowderCalculations.calculateAverageDensity);
        }
    });
    
    // Битумоемкость
    ['bitumen_capacity_weight', 'bitumen_capacity_weight_after', 'bitumen_capacity_oil_weight', 'bitumen_capacity_real_density'].forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', window.mineralPowderCalculations.calculateBitumenCapacity);
            element.addEventListener('change', window.mineralPowderCalculations.calculateBitumenCapacity);
        }
    });
    
    // Выполняем начальные расчеты
    setTimeout(function() {
        console.log('Выполняем начальные расчеты...');
        window.mineralPowderCalculations.calculateCompounds();
        window.mineralPowderCalculations.calculateHumidity();
        window.mineralPowderCalculations.calculateRealDensity(1);
        window.mineralPowderCalculations.calculateRealDensity(2);
        window.mineralPowderCalculations.calculateAverageDensity();
        window.mineralPowderCalculations.calculateBitumenCapacity();
    }, 100);
    
    // Блокировка Enter и стрелок
    const form = document.getElementById('mineral-powder-form');
    if (form) {
        form.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.keyCode === 40 || e.keyCode === 38) {
                e.preventDefault();
            }
        });
    }
    
    console.log('Скрипт расчетов для минерального порошка ГОСТ 32761-2014 загружен и готов к работе');
});
