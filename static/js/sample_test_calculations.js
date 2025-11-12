// Функция для расчета остатка на сите 8 мм
function calculateGrainsMore8() {
    console.log('calculateGrainsMore8 called');
    const initialWeight = document.getElementById('grain_initial_weight');
    const weight8 = document.getElementById('grain_8_weight');
    const percent8 = document.getElementById('grain_8_percent');
    const hidden8 = document.getElementById('grain_8_percent_hidden');
    
    console.log('Fields found:', {
        initialWeight: !!initialWeight,
        weight8: !!weight8,
        percent8: !!percent8,
        values: {
            initial: initialWeight?.value,
            w8: weight8?.value
        }
    });
    
    if (initialWeight && weight8 && percent8 && initialWeight.value && weight8.value) {
        const initial = parseFloat(initialWeight.value);
        const w8 = parseFloat(weight8.value);
        
        if (!isNaN(initial) && !isNaN(w8) && initial > 0) {
            const percentage = Math.round((w8 / initial) * 100 * 100) / 100;
            console.log(`Calculated: ${w8} / ${initial} * 100 = ${percentage}%`);
            percent8.value = percentage;
            if (hidden8) hidden8.value = percentage;
            
            // Убираем класс input-alert после расчета
            percent8.classList.remove('input-alert');
        }
    }
}

// Функция для расчета остатка на сите 4 мм
function calculateGrainsMore4() {
    const initialWeight = document.getElementById('grain_initial_weight');
    const weight4 = document.getElementById('grain_4_weight');
    const percent4 = document.getElementById('grain_4_percent');
    const hidden4 = document.getElementById('grain_4_percent_hidden');
    
    if (initialWeight && weight4 && percent4 && initialWeight.value && weight4.value) {
        const initial = parseFloat(initialWeight.value);
        const w4 = parseFloat(weight4.value);
        
        if (!isNaN(initial) && !isNaN(w4) && initial > 0) {
            const percentage = Math.round((w4 / initial) * 100 * 100) / 100;
            percent4.value = percentage;
            if (hidden4) hidden4.value = percentage;
            
            // Убираем класс input-alert после расчета
            percent4.classList.remove('input-alert');
        }
    }
}

// Функция для расчета содержания пылевидных и глинистых частиц
function calculateDustAndClay() {
    const initialWeight = document.getElementById('dust_initial_weight');
    const afterWeight = document.getElementById('dust_after_weight');
    const percent = document.getElementById('dust_percent');
    const hidden = document.getElementById('dust_percent_hidden');
    
    if (initialWeight && afterWeight && percent && initialWeight.value && afterWeight.value) {
        const initial = parseFloat(initialWeight.value);
        const after = parseFloat(afterWeight.value);
        
        if (!isNaN(initial) && !isNaN(after) && initial > 0) {
            const percentage = Math.round(((initial - after) / initial) * 100 * 10) / 10;
            percent.value = percentage;
            if (hidden) hidden.value = percentage;
        }
    }
}

// Функция для расчета частных и полных остатков на ситах
function calculatePartitions() {
    const dustInitial = document.getElementById('dust_initial_weight');
    
    if (!dustInitial || !dustInitial.value) return;
    
    const initial = parseFloat(dustInitial.value);
    if (isNaN(initial) || initial <= 0) return;
    
    const sieves = ['2', '1', '05', '025', '0125'];
    let previousFull = 0;
    
    for (let i = 0; i < sieves.length; i++) {
        const sieve = sieves[i];
        const weight = document.getElementById(`sieve_${sieve}_weight`);
        const partial = document.getElementById(`sieve_${sieve}_partial`);
        const full = document.getElementById(`sieve_${sieve}_full`);
        const partialHidden = document.getElementById(`sieve_${sieve}_partial_hidden`);
        const fullHidden = document.getElementById(`sieve_${sieve}_full_hidden`);
        
        if (weight && partial && full && weight.value) {
            const w = parseFloat(weight.value);
            
            if (!isNaN(w)) {
                // Частный остаток
                const partialValue = Math.round((w / initial) * 100 * 10) / 10;
                partial.value = partialValue;
                if (partialHidden) partialHidden.value = partialValue;
                
                // Полный остаток
                const fullValue = Math.round((partialValue + previousFull) * 10) / 10;
                full.value = fullValue;
                if (fullHidden) fullHidden.value = fullValue;
                
                previousFull = fullValue;
            }
        }
    }
    
    calculateSizeModule();
}

// Функция для расчета модуля крупности
function calculateSizeModule() {
    const fullValues = [];
    const sieves = ['2', '1', '05', '025', '0125'];
    
    for (const sieve of sieves) {
        const full = document.getElementById(`sieve_${sieve}_full`);
        if (full && full.value) {
            fullValues.push(parseFloat(full.value));
        }
    }
    
    if (fullValues.length === 5) {
        const sum = fullValues.reduce((a, b) => a + b, 0);
        const module = Math.round(sum / 100 * 100) / 100;
        
        const moduleValue = document.getElementById('size_module_value');
        const moduleName = document.getElementById('size_module_name');
        const moduleValueHidden = document.getElementById('size_module_value_hidden');
        const moduleNameHidden = document.getElementById('size_module_name_hidden');
        
        if (moduleValue) {
            moduleValue.value = module;
            if (moduleValueHidden) moduleValueHidden.value = module;
        }
        
        if (moduleName) {
            let name = '';
            if (module <= 1.5) name = 'Очень мелкий';
            else if (module <= 2.0) name = 'Мелкий';
            else if (module <= 2.5) name = 'Средний';
            else if (module <= 3.0) name = 'Крупный';
            else name = 'Очень крупный';
            
            moduleName.value = name;
            if (moduleNameHidden) moduleNameHidden.value = name;
        }
    }
}

// Функция для расчета содержания глины в комках
function calculateClay() {
    const initialWeight = document.getElementById('clay_initial_weight');
    const clayWeight = document.getElementById('clay_weight');
    const percent = document.getElementById('clay_percent');
    const hidden = document.getElementById('clay_percent_hidden');
    
    if (initialWeight && clayWeight && percent && initialWeight.value && clayWeight.value) {
        const initial = parseFloat(initialWeight.value);
        const clay = parseFloat(clayWeight.value);
        
        if (!isNaN(initial) && !isNaN(clay) && initial > 0) {
            const percentage = Math.round((clay / initial) * 100 * 100) / 100;
            percent.value = percentage;
            if (hidden) hidden.value = percentage;
        }
    }
}

// Функция для расчета влажности
function calculateHumidity(index) {
    const container = document.getElementById(`humidity_${index}_container`);
    const withSand = document.getElementById(`humidity_${index}_with_sand`);
    const afterDry = document.getElementById(`humidity_${index}_after_dry`);
    const value = document.getElementById(`humidity_${index}_value`);
    const hidden = document.getElementById(`humidity_${index}_value_hidden`);
    
    if (container && withSand && afterDry && value) {
        const c = parseFloat(container.value);
        const ws = parseFloat(withSand.value);
        const ad = parseFloat(afterDry.value);
        
        if (!isNaN(c) && !isNaN(ws) && !isNaN(ad) && (ad - c) > 0) {
            const humidity = Math.round(((ws - ad) / (ad - c)) * 100 * 10) / 10;
            value.value = humidity;
            if (hidden) hidden.value = humidity;
            
            calculateAverageHumidity();
        }
    }
}

// Функция для расчета средней влажности
function calculateAverageHumidity() {
    const h1 = document.getElementById('humidity_1_value');
    const h2 = document.getElementById('humidity_2_value');
    const average = document.getElementById('humidity_average');
    const hidden = document.getElementById('humidity_average_hidden');
    
    if (h1 && h2 && average && h1.value && h2.value) {
        const v1 = parseFloat(h1.value);
        const v2 = parseFloat(h2.value);
        
        if (!isNaN(v1) && !isNaN(v2)) {
            const avg = Math.round((v1 + v2) / 2 * 10) / 10;
            average.value = avg;
            if (hidden) hidden.value = avg;
        }
    }
}

// Функция для расчета приращения объема глинистых частиц
function calculateClayConsistance(index) {
    const initial = document.getElementById(`clay_swell_${index}_initial`);
    const after = document.getElementById(`clay_swell_${index}_after`);
    const k = document.getElementById(`clay_swell_${index}_k`);
    const hidden = document.getElementById(`clay_swell_${index}_k_hidden`);
    
    if (initial && after && k && initial.value && after.value) {
        const i = parseFloat(initial.value);
        const a = parseFloat(after.value);
        
        if (!isNaN(i) && !isNaN(a) && i > 0) {
            const kValue = Math.round((a - i) / i * 100) / 100;
            k.value = kValue;
            if (hidden) hidden.value = kValue;
            
            calculateAverageVolumeIncrement();
        }
    }
}

// Функция для расчета среднего приращения объема
function calculateAverageVolumeIncrement() {
    const k1 = document.getElementById('clay_swell_1_k');
    const k2 = document.getElementById('clay_swell_2_k');
    const average = document.getElementById('clay_swell_average_k');
    const hidden = document.getElementById('clay_swell_average_k_hidden');
    
    if (k1 && k2 && average && k1.value && k2.value) {
        const v1 = parseFloat(k1.value);
        const v2 = parseFloat(k2.value);
        
        if (!isNaN(v1) && !isNaN(v2)) {
            if (Math.abs(v1 - v2) > 0.02) {
                k1.classList.add('input-alert');
                k2.classList.add('input-alert');
                average.value = '';
                if (hidden) hidden.value = '';
            } else {
                k1.classList.remove('input-alert');
                k2.classList.remove('input-alert');
                const avg = Math.round((v1 + v2) / 2 * 100) / 100;
                average.value = avg;
                if (hidden) hidden.value = avg;
                
                // Здесь можно добавить расчет содержания глинистых частиц
                // calculateClayConsistanceValue();
            }
        }
    }
}

// Функция для расчета насыпной плотности
function calculateBulkDensity(index) {
    const volume = document.getElementById(`bulk_${index}_volume`);
    const empty = document.getElementById(`bulk_${index}_empty`);
    const full = document.getElementById(`bulk_${index}_full`);
    const density = document.getElementById(`bulk_${index}_density`);
    const hidden = document.getElementById(`bulk_${index}_density_hidden`);
    
    if (volume && empty && full && density) {
        const v = parseFloat(volume.value);
        const e = parseFloat(empty.value);
        const f = parseFloat(full.value);
        
        if (!isNaN(v) && !isNaN(e) && !isNaN(f) && v > 0) {
            const d = Math.round((f - e) / v * 100) / 100;
            density.value = d;
            if (hidden) hidden.value = d;
            
            calculateAverageBulkDensity();
        }
    }
}

// Функция для расчета средней насыпной плотности
function calculateAverageBulkDensity() {
    const d1 = document.getElementById('bulk_1_density');
    const d2 = document.getElementById('bulk_2_density');
    const average = document.getElementById('bulk_average_density');
    const hidden = document.getElementById('bulk_average_density_hidden');
    
    if (d1 && d2 && average && d1.value && d2.value) {
        const v1 = parseFloat(d1.value);
        const v2 = parseFloat(d2.value);
        
        if (!isNaN(v1) && !isNaN(v2)) {
            if (Math.abs(v1 - v2) > 0.1) {
                d1.classList.add('input-alert');
                d2.classList.add('input-alert');
                average.value = '';
                if (hidden) hidden.value = '';
            } else {
                d1.classList.remove('input-alert');
                d2.classList.remove('input-alert');
                const avg = Math.round((v1 + v2) / 2 * 100) / 100;
                average.value = avg;
                if (hidden) hidden.value = avg;
                
                calculateEmptiness();
            }
        }
    }
}

// Функция для расчета истинной плотности
function calculateActualDensity(index) {
    const empty = document.getElementById(`actual_${index}_empty`);
    const water = document.getElementById(`actual_${index}_water`);
    const sand = document.getElementById(`actual_${index}_sand`);
    const full = document.getElementById(`actual_${index}_full`);
    const density = document.getElementById(`actual_${index}_density`);
    const hidden = document.getElementById(`actual_${index}_density_hidden`);
    
    if (empty && water && sand && full && density) {
        const e = parseFloat(empty.value);
        const w = parseFloat(water.value);
        const s = parseFloat(sand.value);
        const f = parseFloat(full.value);
        
        if (!isNaN(e) && !isNaN(w) && !isNaN(s) && !isNaN(f)) {
            const denominator = (s - e) + (w - f);
            if (denominator > 0) {
                const d = Math.round((s - e) / denominator * 100) / 100;
                density.value = d;
                if (hidden) hidden.value = d;
                
                calculateAverageActualDensity();
            }
        }
    }
}

// Функция для расчета средней истинной плотности
function calculateAverageActualDensity() {
    const d1 = document.getElementById('actual_1_density');
    const d2 = document.getElementById('actual_2_density');
    const average = document.getElementById('actual_average_density');
    const hidden = document.getElementById('actual_average_density_hidden');
    
    if (d1 && d2 && average && d1.value && d2.value) {
        const v1 = parseFloat(d1.value);
        const v2 = parseFloat(d2.value);
        
        if (!isNaN(v1) && !isNaN(v2)) {
            const avg = Math.round((v1 + v2) / 2 * 100) / 100;
            average.value = avg;
            if (hidden) hidden.value = avg;
            
            calculateEmptiness();
        }
    }
}

// Функция для расчета пустотности
function calculateEmptiness() {
    const actualDensity = document.getElementById('actual_average_density');
    const bulkDensity = document.getElementById('bulk_average_density');
    const emptiness = document.getElementById('emptiness');
    const hidden = document.getElementById('emptiness_hidden');
    
    if (actualDensity && bulkDensity && emptiness && actualDensity.value && bulkDensity.value) {
        const actual = parseFloat(actualDensity.value);
        const bulk = parseFloat(bulkDensity.value);
        
        if (!isNaN(actual) && !isNaN(bulk) && actual > 0) {
            const e = Math.round((actual - bulk) / actual * 100 * 100) / 100;
            emptiness.value = e;
            if (hidden) hidden.value = e;
        }
    }
}

// Функция синхронизации всех скрытых полей
function syncAllHiddenFields() {
    const fieldsToSync = [
        'grain_8_percent', 'grain_4_percent', 'dust_percent',
        'sieve_2_partial', 'sieve_1_partial', 'sieve_05_partial', 'sieve_025_partial', 'sieve_0125_partial',
        'sieve_2_full', 'sieve_1_full', 'sieve_05_full', 'sieve_025_full', 'sieve_0125_full',
        'size_module_value', 'size_module_name', 'clay_percent',
        'humidity_1_value', 'humidity_2_value', 'humidity_average',
        'clay_swell_1_k', 'clay_swell_2_k', 'clay_swell_average_k',
        'clay_swell_content', 'clay_swell_conclusion',
        'bulk_1_density', 'bulk_2_density', 'bulk_average_density',
        'actual_1_density', 'actual_2_density', 'actual_average_density',
        'emptiness'
    ];
    
    fieldsToSync.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        const hidden = document.getElementById(fieldId + '_hidden');
        
        if (field && hidden && field.value) {
            hidden.value = field.value;
        }
    });
}

// Функция для запуска всех расчетов
function runAllCalculations() {
    console.log('=== Running all calculations ===');
    
    // Проверяем наличие ключевых полей
    const testFields = [
        'grain_initial_weight',
        'grain_8_weight',
        'grain_8_percent',
        'dust_initial_weight',
        'sieve_2_weight'
    ];
    
    console.log('Checking fields existence:');
    testFields.forEach(id => {
        const elem = document.getElementById(id);
        console.log(`  ${id}: ${elem ? 'EXISTS' : 'NOT FOUND'}`);
    });
    
    // Запускаем все расчеты
    console.log('Starting calculations...');
    calculateGrainsMore4();
    calculateGrainsMore8();
    calculateDustAndClay();
    calculatePartitions();
    calculateClay();
    calculateHumidity();
    calculateClaySwelling();
    calculateBulkDensity();
    calculateActualDensity();
    calculateEmptiness();
    
    // Расчеты для парных значений
    for (let i = 1; i <= 2; i++) {
        calculateHumidity(i);
        calculateClayConsistance(i);
        calculateBulkDensity(i);
        calculateActualDensity(i);
    }
    
    // Синхронизация всех полей
    syncAllHiddenFields();
    
    console.log('All calculations completed');
}

// Проверка загрузки скрипта
console.log('sample_test_calculations.js loaded successfully!');

// Запускаем расчеты сразу при загрузке скрипта
(function() {
    console.log('Starting initial calculations...');
    setTimeout(function() {
        runAllCalculations();
    }, 100);
})();

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, setting up event handlers...');
    
    // Проверяем, есть ли данные в полях при загрузке
    console.log('=== ПРОВЕРКА ЗАГРУЖЕННЫХ ДАННЫХ ===');
    const checkFields = [
        'grain_initial_weight',
        'grain_8_weight', 
        'grain_4_weight',
        'grain_8_percent',
        'grain_4_percent'
    ];
    
    checkFields.forEach(id => {
        const field = document.getElementById(id);
        if (field) {
            console.log(`${id}: value="${field.value}" (${field.value ? 'есть данные' : 'пусто'})`);
        } else {
            console.log(`${id}: НЕ НАЙДЕНО`);
        }
    });
    console.log('===');
    
    // Запускаем расчеты еще раз после загрузки DOM
    setTimeout(function() {
        console.log('Запускаем расчеты после загрузки...');
        runAllCalculations();
    }, 500);
    
    // Добавляем обработчики на поля для зерен 8 и 4 мм
    const grainInitial = document.getElementById('grain_initial_weight');
    if (grainInitial) {
        grainInitial.addEventListener('input', function() {
            calculateGrainsMore4();
            calculateGrainsMore8();
        });
    }
    
    const grain8 = document.getElementById('grain_8_weight');
    if (grain8) {
        grain8.addEventListener('input', calculateGrainsMore8);
    }
    
    const grain4 = document.getElementById('grain_4_weight');
    if (grain4) {
        grain4.addEventListener('input', calculateGrainsMore4);
    }
    
    // Обработчики для пыли и глины
    const dustInitial = document.getElementById('dust_initial_weight');
    if (dustInitial) {
        dustInitial.addEventListener('input', function() {
            calculateDustAndClay();
            calculatePartitions();
        });
    }
    
    const dustAfter = document.getElementById('dust_after_weight');
    if (dustAfter) {
        dustAfter.addEventListener('input', calculateDustAndClay);
    }
    
    // Обработчики для сит
    const sieves = ['2', '1', '05', '025', '0125'];
    sieves.forEach(sieve => {
        const weight = document.getElementById(`sieve_${sieve}_weight`);
        if (weight) {
            weight.addEventListener('input', calculatePartitions);
        }
    });
    
    // Обработчики для глины
    const clayInitial = document.getElementById('clay_initial_weight');
    if (clayInitial) {
        clayInitial.addEventListener('input', calculateClay);
    }
    
    const clayWeight = document.getElementById('clay_weight');
    if (clayWeight) {
        clayWeight.addEventListener('input', calculateClay);
    }
    
    // Обработчики для влажности
    for (let i = 1; i <= 2; i++) {
        ['container', 'with_sand', 'after_dry'].forEach(field => {
            const elem = document.getElementById(`humidity_${i}_${field}`);
            if (elem) {
                elem.addEventListener('input', () => calculateHumidity(i));
            }
        });
    }
    
    // Обработчики для набухания глины
    for (let i = 1; i <= 2; i++) {
        ['initial', 'after'].forEach(field => {
            const elem = document.getElementById(`clay_swell_${i}_${field}`);
            if (elem) {
                elem.addEventListener('input', () => calculateClayConsistance(i));
            }
        });
    }
    
    // Обработчики для насыпной плотности
    for (let i = 1; i <= 2; i++) {
        ['volume', 'empty', 'full'].forEach(field => {
            const elem = document.getElementById(`bulk_${i}_${field}`);
            if (elem) {
                elem.addEventListener('input', () => calculateBulkDensity(i));
            }
        });
    }
    
    // Обработчики для истинной плотности
    for (let i = 1; i <= 2; i++) {
        ['empty', 'water', 'sand', 'full'].forEach(field => {
            const elem = document.getElementById(`actual_${i}_${field}`);
            if (elem) {
                elem.addEventListener('input', () => calculateActualDensity(i));
            }
        });
    }
    
    // Обработчик отправки формы
    const form = document.getElementById('result');
    if (form) {
        form.addEventListener('submit', function(e) {
            console.log('Form submitting, syncing all fields...');
            syncAllHiddenFields();
        });
    }
    
    // Добавляем кнопку для ручного пересчета (для отладки)
    const recalcButton = document.createElement('button');
    recalcButton.type = 'button';
    recalcButton.textContent = 'Пересчитать все';
    recalcButton.style.cssText = 'position: fixed; bottom: 20px; right: 20px; background: #007bff; color: white; border: none; padding: 10px 20px; cursor: pointer; z-index: 1000; border-radius: 5px;';
    recalcButton.onclick = runAllCalculations;
    document.body.appendChild(recalcButton);
});
