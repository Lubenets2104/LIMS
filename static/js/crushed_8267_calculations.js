// Автоматические расчеты для щебня по ГОСТ 8267-93
(function() {
    'use strict';
    
    console.log('crushed_8267_calculations.js loaded');
    
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
            { id: 'sieve_70', size: '70' },
            { id: 'sieve_40', size: '40' },
            { id: 'sieve_20', size: '20' },
            { id: 'sieve_10', size: '10' },
            { id: 'sieve_5', size: '5' },
            { id: 'sieve_2_5', size: '2.5' },
            { id: 'sieve_1_25', size: '1.25' }
        ];
        
        let cumulativePercent = 0;
        
        sieves.forEach((sieve) => {
            const weightField = document.getElementById(sieve.id + '_weight');
            const partialField = document.getElementById(sieve.id + '_partial');
            const fullField = document.getElementById(sieve.id + '_full');
            
            if (!weightField || !partialField || !fullField) {
                console.warn(`Поля для сита ${sieve.size} мм не найдены`);
                return;
            }
            
            const weight = parseFloat(weightField.value) || 0;
            
            // Частный остаток в процентах
            const partialPercent = totalWeight > 0 ? (weight / totalWeight * 100) : 0;
            partialField.value = partialPercent.toFixed(1);
            
            // Полный остаток (накопительный)
            cumulativePercent += partialPercent;
            fullField.value = cumulativePercent.toFixed(1);
            
            console.log(`Сито ${sieve.size}мм: масса=${weight}г, частный=${partialPercent.toFixed(1)}%, полный=${cumulativePercent.toFixed(1)}%`);
        });
        
        // Определяем фракцию на основе полных остатков
        determineFraction();
    }
    
    function determineFraction() {
        // Получаем полные остатки на ситах
        const full_70 = parseFloat(document.getElementById('sieve_70_full')?.value) || 0;
        const full_40 = parseFloat(document.getElementById('sieve_40_full')?.value) || 0;
        const full_20 = parseFloat(document.getElementById('sieve_20_full')?.value) || 0;
        const full_10 = parseFloat(document.getElementById('sieve_10_full')?.value) || 0;
        const full_5 = parseFloat(document.getElementById('sieve_5_full')?.value) || 0;
        const full_2_5 = parseFloat(document.getElementById('sieve_2_5_full')?.value) || 0;
        
        let fraction = '';
        
        // Определяем фракцию по ГОСТ 8267-93
        // Основные фракции: 5-10, 10-20, 20-40, 40-70
        
        if (full_5 <= 5 && full_10 >= 90 && full_10 <= 100) {
            fraction = '5-10';
        } else if (full_10 <= 5 && full_20 >= 90 && full_20 <= 100) {
            fraction = '10-20';
        } else if (full_20 <= 5 && full_40 >= 90 && full_40 <= 100) {
            fraction = '20-40';
        } else if (full_40 <= 5 && full_70 >= 90 && full_70 <= 100) {
            fraction = '40-70';
        } else if (full_5 <= 5 && full_20 >= 90 && full_20 <= 100) {
            fraction = '5-20';
        } else if (full_10 <= 5 && full_40 >= 90 && full_40 <= 100) {
            fraction = '10-40';
        } else {
            fraction = 'Не определена';
        }
        
        const fractionField = document.getElementById('fraction_type');
        if (fractionField) {
            fractionField.value = fraction;
            console.log('Определена фракция:', fraction);
        }
    }
    
    // ===========================
    // ПЫЛЕВИДНЫЕ И ГЛИНИСТЫЕ ЧАСТИЦЫ
    // ===========================
    
    function calculateDustContent() {
        const initialWeight = parseFloat(document.getElementById('dust_initial_weight')?.value) || 0;
        const afterWeight = parseFloat(document.getElementById('dust_after_weight')?.value) || 0;
        const contentField = document.getElementById('dust_content');
        
        if (!contentField) {
            console.warn('Поле для содержания п/г частиц не найдено');
            return;
        }
        
        if (initialWeight <= 0) {
            contentField.value = '';
            return;
        }
        
        // Расчет содержания пылевидных и глинистых частиц
        const dustContent = ((initialWeight - afterWeight) / initialWeight) * 100;
        contentField.value = dustContent.toFixed(2);
        
        console.log(`Содержание п/г частиц: ${dustContent.toFixed(2)}%`);
    }
    
    // ===========================
    // ГЛИНА В КОМКАХ
    // ===========================
    
    function calculateClayContent() {
        const initialWeight = parseFloat(document.getElementById('clay_initial_weight')?.value) || 0;
        const clayWeight = parseFloat(document.getElementById('clay_weight')?.value) || 0;
        const contentField = document.getElementById('clay_content');
        
        if (!contentField) {
            console.warn('Поле для содержания глины в комках не найдено');
            return;
        }
        
        if (initialWeight <= 0) {
            contentField.value = '';
            return;
        }
        
        // Расчет содержания глины в комках
        const clayContent = (clayWeight / initialWeight) * 100;
        contentField.value = clayContent.toFixed(2);
        
        console.log(`Содержание глины в комках: ${clayContent.toFixed(2)}%`);
    }
    
    // ===========================
    // ЛЕЩАДНОСТЬ
    // ===========================
    
    function calculateFlakiness() {
        const fractions = ['5_10', '10_20', '20_40'];
        let totalWeight = 0;
        let totalFlakyWeight = 0;
        
        fractions.forEach(fraction => {
            const weightField = document.getElementById(`flakiness_${fraction}_weight`);
            const flakyWeightField = document.getElementById(`flakiness_${fraction}_flaky_weight`);
            const valueField = document.getElementById(`flakiness_${fraction}_value`);
            
            if (!weightField || !flakyWeightField || !valueField) {
                return;
            }
            
            const weight = parseFloat(weightField.value) || 0;
            const flakyWeight = parseFloat(flakyWeightField.value) || 0;
            
            if (weight > 0) {
                const flakiness = (flakyWeight / weight) * 100;
                valueField.value = flakiness.toFixed(2);
                
                totalWeight += weight;
                totalFlakyWeight += flakyWeight;
                
                console.log(`Лещадность фракции ${fraction}: ${flakiness.toFixed(2)}%`);
            } else {
                valueField.value = '';
            }
        });
        
        // Расчет средневзвешенной лещадности
        const averageField = document.getElementById('flakiness_average');
        const groupField = document.getElementById('flakiness_group');
        
        if (averageField && groupField && totalWeight > 0) {
            const averageFlakiness = (totalFlakyWeight / totalWeight) * 100;
            averageField.value = averageFlakiness.toFixed(2);
            
            // Определение группы по лещадности согласно ГОСТ 8267-93
            let group = '';
            if (averageFlakiness <= 10) {
                group = 'I';  // Кубовидная
            } else if (averageFlakiness <= 15) {
                group = 'II';  // Улучшенная
            } else if (averageFlakiness <= 25) {
                group = 'III';  // Обычная
            } else if (averageFlakiness <= 35) {
                group = 'IV';
            } else if (averageFlakiness <= 50) {
                group = 'V';
            } else {
                group = 'Не соотв.';
            }
            
            groupField.value = group;
            console.log(`Средняя лещадность: ${averageFlakiness.toFixed(2)}%, группа: ${group}`);
        }
    }
    
    // ===========================
    // ДРОБИМОСТЬ
    // ===========================
    
    function calculateCrushability() {
        const fractions = ['5_10', '10_20', '20_40'];
        const rockType = parseInt(document.getElementById('crushability_type')?.value) || 0;
        let totalWeight = 0;
        let totalLoss = 0;
        
        fractions.forEach(fraction => {
            const weightField = document.getElementById(`crushability_${fraction}_weight`);
            const afterWeightField = document.getElementById(`crushability_${fraction}_after_weight`);
            const valueField = document.getElementById(`crushability_${fraction}_value`);
            
            if (!weightField || !afterWeightField || !valueField) {
                return;
            }
            
            const weight = parseFloat(weightField.value) || 0;
            const afterWeight = parseFloat(afterWeightField.value) || 0;
            
            if (weight > 0) {
                const crushability = ((weight - afterWeight) / weight) * 100;
                valueField.value = crushability.toFixed(2);
                
                totalWeight += weight;
                totalLoss += (weight - afterWeight);
                
                console.log(`Дробимость фракции ${fraction}: ${crushability.toFixed(2)}%`);
            } else {
                valueField.value = '';
            }
        });
        
        // Расчет средневзвешенной дробимости
        const averageField = document.getElementById('crushability_average');
        const markField = document.getElementById('crushability_mark');
        
        if (averageField && markField && totalWeight > 0) {
            const averageCrushability = (totalLoss / totalWeight) * 100;
            averageField.value = averageCrushability.toFixed(2);
            
            // Определение марки по дробимости согласно ГОСТ 8267-93
            let mark = '';
            
            if (rockType === 0) {
                // Изверженные и метаморфические породы
                if (averageCrushability <= 8) {
                    mark = 'М1400';
                } else if (averageCrushability <= 12) {
                    mark = 'М1200';
                } else if (averageCrushability <= 16) {
                    mark = 'М1000';
                } else if (averageCrushability <= 20) {
                    mark = 'М800';
                } else if (averageCrushability <= 25) {
                    mark = 'М600';
                } else if (averageCrushability <= 34) {
                    mark = 'М400';
                } else if (averageCrushability <= 42) {
                    mark = 'М300';
                } else if (averageCrushability <= 52) {
                    mark = 'М200';
                } else {
                    mark = 'Не соответствует';
                }
            } else {
                // Осадочные породы
                if (averageCrushability <= 10) {
                    mark = 'М1200';
                } else if (averageCrushability <= 14) {
                    mark = 'М1000';
                } else if (averageCrushability <= 18) {
                    mark = 'М800';
                } else if (averageCrushability <= 24) {
                    mark = 'М600';
                } else if (averageCrushability <= 30) {
                    mark = 'М400';
                } else if (averageCrushability <= 40) {
                    mark = 'М300';
                } else if (averageCrushability <= 47) {
                    mark = 'М200';
                } else {
                    mark = 'Не соответствует';
                }
            }
            
            markField.value = mark;
            console.log(`Средняя дробимость: ${averageCrushability.toFixed(2)}%, марка: ${mark}`);
        }
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
            'sieve_70_weight', 'sieve_40_weight', 'sieve_20_weight',
            'sieve_10_weight', 'sieve_5_weight', 'sieve_2_5_weight', 'sieve_1_25_weight'
        ];
        
        sieveFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('input', calculateGrainCompound);
            }
        });
        
        // Привязка обработчиков для пылевидных и глинистых частиц
        const dustFields = ['dust_initial_weight', 'dust_after_weight'];
        dustFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('input', calculateDustContent);
            }
        });
        
        // Привязка обработчиков для глины в комках
        const clayFields = ['clay_initial_weight', 'clay_weight'];
        clayFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('input', calculateClayContent);
            }
        });
        
        // Привязка обработчиков для лещадности
        const flakinessFields = [
            'flakiness_5_10_weight', 'flakiness_5_10_flaky_weight',
            'flakiness_10_20_weight', 'flakiness_10_20_flaky_weight',
            'flakiness_20_40_weight', 'flakiness_20_40_flaky_weight'
        ];
        
        flakinessFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('input', calculateFlakiness);
            }
        });
        
        // Привязка обработчиков для дробимости
        const crushabilityFields = [
            'crushability_5_10_weight', 'crushability_5_10_after_weight',
            'crushability_10_20_weight', 'crushability_10_20_after_weight',
            'crushability_20_40_weight', 'crushability_20_40_after_weight',
            'crushability_type'
        ];
        
        crushabilityFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('input', calculateCrushability);
                field.addEventListener('change', calculateCrushability);
            }
        });
        
        // Выполняем начальные расчеты при загрузке страницы
        calculateGrainCompound();
        calculateDustContent();
        calculateClayContent();
        calculateFlakiness();
        calculateCrushability();
        
        console.log('Расчеты для ГОСТ 8267-93 инициализированы');
    }
    
    // Запускаем инициализацию при загрузке DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeCalculations);
    } else {
        initializeCalculations();
    }
    
})();
