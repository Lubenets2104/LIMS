// Расчеты для ЩПС по ГОСТ 25607-2009

document.addEventListener('DOMContentLoaded', function() {
    console.log('Инициализация расчетов ЩПС');
    
    // === СОДЕРЖАНИЕ ПЫЛЕВИДНЫХ И ГЛИНИСТЫХ ЧАСТИЦ ===
    const dustInitialInput = document.getElementById('dust_initial_weight');
    const dustAfterWashInput = document.getElementById('dust_after_wash_weight');
    const dustClayContentInput = document.getElementById('dust_clay_content');
    
    function calculateDustClayContent() {
        const initial = parseFloat(dustInitialInput.value) || 0;
        const afterWash = parseFloat(dustAfterWashInput.value) || 0;
        
        if (initial > 0 && afterWash >= 0 && afterWash <= initial) {
            const content = ((initial - afterWash) / initial) * 100;
            dustClayContentInput.value = content.toFixed(1);
        } else {
            dustClayContentInput.value = '';
        }
        
        // Запускаем расчет зернового состава после обновления массы
        calculateGrainComposition();
    }
    
    if (dustInitialInput && dustAfterWashInput) {
        dustInitialInput.addEventListener('input', calculateDustClayContent);
        dustAfterWashInput.addEventListener('input', calculateDustClayContent);
    }
    
    // === ЗЕРНОВОЙ СОСТАВ ===
    const sieves = ['40', '20', '10', '5', '2_5', '0_63', '0_16', '0_05'];
    const gostRanges = {
        '40': {min: 0, max: 10},
        '20': {min: 20, max: 40},
        '10': {min: 35, max: 60},
        '5': {min: 45, max: 70},
        '2_5': {min: 55, max: 80},
        '0_63': {min: 70, max: 90},
        '0_16': {min: 75, max: 92},
        '0_05': {min: 80, max: 93}
    };
    
    function calculateGrainComposition() {
        const initialWeight = parseFloat(dustInitialInput.value) || 0;
        
        if (initialWeight <= 0) return;
        
        let cumulativeFull = 0;
        
        sieves.forEach((sieve, index) => {
            const weightInput = document.getElementById(`sieve_${sieve}_weight`);
            const partialInput = document.getElementById(`sieve_${sieve}_partial`);
            const fullInput = document.getElementById(`sieve_${sieve}_full`);
            
            if (weightInput && partialInput && fullInput) {
                const weight = parseFloat(weightInput.value) || 0;
                
                // Частный остаток
                const partial = (weight / initialWeight) * 100;
                partialInput.value = partial > 0 ? partial.toFixed(1) : '';
                
                // Полный остаток
                cumulativeFull += partial;
                fullInput.value = cumulativeFull > 0 ? cumulativeFull.toFixed(1) : '';
                
                // Проверка на соответствие ГОСТ
                if (cumulativeFull > 0) {
                    const range = gostRanges[sieve];
                    if (cumulativeFull < range.min || cumulativeFull > range.max) {
                        fullInput.classList.add('input-alert');
                    } else {
                        fullInput.classList.remove('input-alert');
                    }
                }
            }
        });
    }
    
    // Добавляем обработчики для всех полей массы сит
    sieves.forEach(sieve => {
        const weightInput = document.getElementById(`sieve_${sieve}_weight`);
        if (weightInput) {
            weightInput.addEventListener('input', calculateGrainComposition);
        }
    });
    
    // === ДРОБИМОСТЬ ===
    const fragilityFractions = ['40_70', '20_40', '10_20', '5_10'];
    
    function calculateFragility(fraction) {
        const initialInput = document.getElementById(`fragility_${fraction}_initial`);
        const afterInput = document.getElementById(`fragility_${fraction}_after`);
        const valueInput = document.getElementById(`fragility_${fraction}_value`);
        
        if (initialInput && afterInput && valueInput) {
            const initial = parseFloat(initialInput.value) || 0;
            const after = parseFloat(afterInput.value) || 0;
            
            if (initial > 0 && after >= 0 && after <= initial) {
                const fragility = ((initial - after) / initial) * 100;
                valueInput.value = fragility.toFixed(1);
            } else {
                valueInput.value = '';
            }
            
            // Пересчитываем суммарную дробимость
            calculateFragilitySummary();
        }
    }
    
    function calculateFragilitySummary() {
        let weightedSum = 0;
        let totalWeight = 0;
        
        // Получаем полные остатки первых 4 фракций (они соответствуют фракциям дробимости)
        const sievesForFragility = ['40', '20', '10', '5'];
        
        fragilityFractions.forEach((fraction, index) => {
            const fragilityValue = parseFloat(document.getElementById(`fragility_${fraction}_value`)?.value) || 0;
            const fullValue = parseFloat(document.getElementById(`sieve_${sievesForFragility[index]}_full`)?.value) || 0;
            
            if (fragilityValue > 0 && fullValue > 0) {
                weightedSum += fragilityValue * fullValue;
                totalWeight += fullValue;
            }
        });
        
        const summaryInput = document.getElementById('fragility_summary');
        if (summaryInput && totalWeight > 0) {
            summaryInput.value = (weightedSum / totalWeight).toFixed(1);
        } else if (summaryInput) {
            summaryInput.value = '';
        }
    }
    
    // Добавляем обработчики для полей дробимости
    fragilityFractions.forEach(fraction => {
        const initialInput = document.getElementById(`fragility_${fraction}_initial`);
        const afterInput = document.getElementById(`fragility_${fraction}_after`);
        
        if (initialInput && afterInput) {
            initialInput.addEventListener('input', () => calculateFragility(fraction));
            afterInput.addEventListener('input', () => calculateFragility(fraction));
        }
    });
    
    // === ЛЕЩАДНОСТЬ ===
    const flakinessFractions = ['40_70', '20_40', '10_20', '5_10'];
    
    function calculateFlakiness(fraction) {
        const initialInput = document.getElementById(`flakiness_${fraction}_initial`);
        const flakyInput = document.getElementById(`flakiness_${fraction}_flaky`);
        const valueInput = document.getElementById(`flakiness_${fraction}_value`);
        
        if (initialInput && flakyInput && valueInput) {
            const initial = parseFloat(initialInput.value) || 0;
            const flaky = parseFloat(flakyInput.value) || 0;
            
            if (initial > 0 && flaky >= 0 && flaky <= initial) {
                const flakiness = (flaky / initial) * 100;
                valueInput.value = flakiness.toFixed(1);
            } else {
                valueInput.value = '';
            }
            
            // Пересчитываем суммарную лещадность
            calculateFlakinessSummary();
        }
    }
    
    function calculateFlakinessSummary() {
        let weightedSum = 0;
        let totalWeight = 0;
        
        // Получаем полные остатки первых 4 фракций (они соответствуют фракциям лещадности)
        const sievesForFlakiness = ['40', '20', '10', '5'];
        
        flakinessFractions.forEach((fraction, index) => {
            const flakinessValue = parseFloat(document.getElementById(`flakiness_${fraction}_value`)?.value) || 0;
            const fullValue = parseFloat(document.getElementById(`sieve_${sievesForFlakiness[index]}_full`)?.value) || 0;
            
            if (flakinessValue > 0 && fullValue > 0) {
                weightedSum += flakinessValue * fullValue;
                totalWeight += fullValue;
            }
        });
        
        const summaryInput = document.getElementById('flakiness_summary');
        if (summaryInput && totalWeight > 0) {
            summaryInput.value = (weightedSum / totalWeight).toFixed(1);
        } else if (summaryInput) {
            summaryInput.value = '';
        }
    }
    
    // Добавляем обработчики для полей лещадности
    flakinessFractions.forEach(fraction => {
        const initialInput = document.getElementById(`flakiness_${fraction}_initial`);
        const flakyInput = document.getElementById(`flakiness_${fraction}_flaky`);
        
        if (initialInput && flakyInput) {
            initialInput.addEventListener('input', () => calculateFlakiness(fraction));
            flakyInput.addEventListener('input', () => calculateFlakiness(fraction));
        }
    });
    
    // Запускаем начальные расчеты при загрузке страницы
    calculateDustClayContent();
    calculateGrainComposition();
    fragilityFractions.forEach(fraction => calculateFragility(fraction));
    flakinessFractions.forEach(fraction => calculateFlakiness(fraction));
    
    console.log('Расчеты ЩПС инициализированы');
});
