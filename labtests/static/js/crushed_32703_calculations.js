// Автоматические расчеты для щебня по ГОСТ 32703-2014 (узкие фракции)
(function() {
    'use strict';
    
    console.log('crushed_32703_calculations.js loaded');
    
    // ===========================
    // ГРАНУЛОМЕТРИЧЕСКИЙ СОСТАВ
    // ===========================
    
    function calculateGrainCompound() {
        const totalWeight = parseFloat(document.getElementById('grain_compound_weight')?.value) || 0;
        
        if (totalWeight <= 0) {
            console.log('Масса пробы не указана или равна нулю');
            return;
        }
        
        // Получаем массы на ситах
        const sieves = [
            { id: 'sieve_2d', name: '2D' },
            { id: 'sieve_1_4d', name: '1.4D' },
            { id: 'sieve_d', name: 'D' },
            { id: 'sieve_d_small', name: 'd' },
            { id: 'sieve_d_2', name: 'd/2' }
        ];
        
        let cumulativePercent = 0;
        
        sieves.forEach((sieve, index) => {
            const weightField = document.getElementById(sieve.id + '_weight');
            const partialField = document.getElementById(sieve.id + '_partial');
            const fullField = document.getElementById(sieve.id + '_full');
            
            if (!weightField || !partialField || !fullField) {
                console.warn(`Поля для сита ${sieve.name} не найдены`);
                return;
            }
            
            const weight = parseFloat(weightField.value) || 0;
            
            // Частный остаток в процентах
            const partialPercent = totalWeight > 0 ? (weight / totalWeight * 100) : 0;
            partialField.value = partialPercent.toFixed(1);
            
            // Накопительный процент (остаток на сите и выше)
            cumulativePercent += partialPercent;
            
            // Проходы через сито (100% минус накопительный остаток)
            const fullPercent = 100 - cumulativePercent;
            fullField.value = fullPercent.toFixed(1);
            
            console.log(`Сито ${sieve.name}: масса=${weight}г, частный=${partialPercent.toFixed(1)}%, проход=${fullPercent.toFixed(1)}%`);
        });
        
        // Определяем марку по проходам через сито
        determineMark();
    }
    
    function determineMark() {
        // Получаем значения проходов через сита
        const passes = {
            '2D': parseFloat(document.getElementById('sieve_2d_full')?.value) || 0,
            '1.4D': parseFloat(document.getElementById('sieve_1_4d_full')?.value) || 0,
            'D': parseFloat(document.getElementById('sieve_d_full')?.value) || 0,
            'd': parseFloat(document.getElementById('sieve_d_small_full')?.value) || 0,
            'd/2': parseFloat(document.getElementById('sieve_d_2_full')?.value) || 0
        };
        
        console.log('Проходы через сита:', passes);
        
        // Определяем марку согласно ГОСТ 32703-2014
        // Марки: 90/10, 90/15, 90/20, 85/15, 85/20, 85/35
        let mark = '';
        
        // Проверяем соответствие каждой марке
        const marks = [
            {
                name: '90/10',
                criteria: {
                    '2D': [100, 100],
                    '1.4D': [100, 100],
                    'D': [90, 100],
                    'd': [0, 10],
                    'd/2': [0, 2]
                }
            },
            {
                name: '90/15',
                criteria: {
                    '2D': [100, 100],
                    '1.4D': [98, 100],
                    'D': [90, 100],
                    'd': [0, 15],
                    'd/2': [0, 5]
                }
            },
            {
                name: '90/20',
                criteria: {
                    '2D': [100, 100],
                    '1.4D': [98, 100],
                    'D': [90, 100],
                    'd': [0, 20],
                    'd/2': [0, 5]
                }
            },
            {
                name: '85/15',
                criteria: {
                    '2D': [100, 100],
                    '1.4D': [98, 100],
                    'D': [85, 100],
                    'd': [0, 15],
                    'd/2': [0, 5]
                }
            },
            {
                name: '85/20',
                criteria: {
                    '2D': [100, 100],
                    '1.4D': [98, 100],
                    'D': [85, 100],
                    'd': [0, 20],
                    'd/2': [0, 5]
                }
            },
            {
                name: '85/35',
                criteria: {
                    '2D': [100, 100],
                    '1.4D': [98, 100],
                    'D': [85, 100],
                    'd': [0, 35],
                    'd/2': [0, 5]
                }
            }
        ];
        
        // Проверяем каждую марку
        for (const markDef of marks) {
            let matches = true;
            
            for (const [sieve, [min, max]] of Object.entries(markDef.criteria)) {
                const value = passes[sieve];
                if (value < min || value > max) {
                    matches = false;
                    break;
                }
            }
            
            if (matches) {
                mark = markDef.name;
                break;
            }
        }
        
        // Если не соответствует ни одной марке
        if (!mark) {
            mark = 'Не соответствует';
        }
        
        const markField = document.getElementById('mark_type');
        if (markField) {
            markField.value = mark;
            console.log('Определена марка:', mark);
        }
    }
    
    // ===========================
    // ЛЕЩАДНОСТЬ
    // ===========================
    
    function calculateFlakiness() {
        const totalWeight = parseFloat(document.getElementById('flakiness_weight')?.value) || 0;
        const flakyWeight = parseFloat(document.getElementById('flakiness_flaky_weight')?.value) || 0;
        const valueField = document.getElementById('flakiness_value');
        const markField = document.getElementById('flakiness_mark');
        
        if (!valueField || !markField) {
            console.warn('Поля для лещадности не найдены');
            return;
        }
        
        if (totalWeight <= 0) {
            valueField.value = '';
            markField.value = '';
            return;
        }
        
        // Расчет лещадности в процентах
        const flakiness = (flakyWeight / totalWeight) * 100;
        valueField.value = flakiness.toFixed(2);
        
        // Определение марки по лещадности согласно ГОСТ 32703-2014
        let mark = '';
        if (flakiness <= 10) {
            mark = 'Л10';
        } else if (flakiness <= 15) {
            mark = 'Л15';
        } else if (flakiness <= 20) {
            mark = 'Л20';
        } else if (flakiness <= 25) {
            mark = 'Л25';
        } else if (flakiness <= 30) {
            mark = 'Л30';
        } else if (flakiness <= 35) {
            mark = 'Л35';
        } else if (flakiness <= 50) {
            mark = 'Л50';
        } else {
            mark = 'Не соответствует';
        }
        
        markField.value = mark;
        console.log(`Лещадность: ${flakiness.toFixed(2)}%, марка: ${mark}`);
    }
    
    // ===========================
    // ДРОБИМОСТЬ
    // ===========================
    
    function calculateCrushability() {
        const totalWeight = parseFloat(document.getElementById('crushability_weight')?.value) || 0;
        const afterWeight = parseFloat(document.getElementById('crushability_after_weight')?.value) || 0;
        const rockType = parseInt(document.getElementById('crushability_type')?.value) || 0;
        const valueField = document.getElementById('crushability_value');
        const markField = document.getElementById('crushability_mark');
        
        if (!valueField || !markField) {
            console.warn('Поля для дробимости не найдены');
            return;
        }
        
        if (totalWeight <= 0) {
            valueField.value = '';
            markField.value = '';
            return;
        }
        
        // Расчет дробимости в процентах
        // Дробимость = ((m1 - m2) / m1) * 100
        // где m1 - начальная масса, m2 - масса после дробления
        const crushability = ((totalWeight - afterWeight) / totalWeight) * 100;
        valueField.value = crushability.toFixed(2);
        
        // Определение марки по дробимости согласно ГОСТ 32703-2014
        let mark = '';
        
        if (rockType === 0) {
            // Изверженные и метаморфические породы, щебень из гравия (испытание в сухом состоянии)
            if (crushability <= 9) {
                mark = 'М1400';  // До 9% включительно
            } else if (crushability <= 11) {
                mark = 'М1200';  // >9% до 11%
            } else if (crushability <= 13) {
                mark = 'М1000';  // >11% до 13%
            } else if (crushability <= 15) {
                mark = 'М800';   // >13% до 15%
            } else if (crushability <= 20) {
                mark = 'М600';   // >15% до 20%
            } else if (crushability <= 25) {
                mark = 'М400';   // >20% до 25%
            } else {
                mark = 'Не соответствует';
            }
        } else {
            // Осадочные породы (испытание в насыщенном водой состоянии)
            if (crushability <= 10) {
                mark = 'М1400';  // До 10% включительно
            } else if (crushability <= 12) {
                mark = 'М1200';  // >10% до 12%
            } else if (crushability <= 15) {
                mark = 'М1000';  // >12% до 15%
            } else if (crushability <= 18) {
                mark = 'М800';   // >15% до 18%
            } else if (crushability <= 22) {
                mark = 'М600';   // >18% до 22%
            } else if (crushability <= 28) {
                mark = 'М400';   // >22% до 28%
            } else {
                mark = 'Не соответствует';
            }
        }
        
        markField.value = mark;
        console.log(`Дробимость: ${crushability.toFixed(2)}%, марка: ${mark}`);
    }
    
    // ===========================
    // ИНИЦИАЛИЗАЦИЯ
    // ===========================
    
    function initializeCalculations() {
        // Привязка обработчиков для гранулометрического состава
        const grainWeightField = document.getElementById('grain_compound_weight');
        if (grainWeightField) {
            grainWeightField.addEventListener('input', calculateGrainCompound);
        }
        
        // Привязка для масс на ситах
        const sieveFields = [
            'sieve_2d_weight', 'sieve_1_4d_weight', 'sieve_d_weight',
            'sieve_d_small_weight', 'sieve_d_2_weight'
        ];
        
        sieveFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('input', calculateGrainCompound);
            }
        });
        
        // Привязка обработчиков для лещадности
        const flakinessFields = ['flakiness_weight', 'flakiness_flaky_weight'];
        flakinessFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('input', calculateFlakiness);
            }
        });
        
        // Привязка обработчиков для дробимости
        const crushabilityFields = ['crushability_weight', 'crushability_after_weight', 'crushability_type'];
        crushabilityFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('input', calculateCrushability);
                field.addEventListener('change', calculateCrushability);
            }
        });
        
        // Выполняем начальные расчеты при загрузке страницы
        calculateGrainCompound();
        calculateFlakiness();
        calculateCrushability();
        
        console.log('Расчеты для ГОСТ 32703-2014 инициализированы');
    }
    
    // Запускаем инициализацию при загрузке DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeCalculations);
    } else {
        initializeCalculations();
    }
    
})();
