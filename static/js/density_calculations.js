// Функция для расчета истинной плотности
function calculateActualDensity() {
    console.log('calculateActualDensity called');
    
    // Первый образец
    const empty1 = document.getElementById('actual_1_empty');
    const water1 = document.getElementById('actual_1_water');
    const sand1 = document.getElementById('actual_1_sand');
    const full1 = document.getElementById('actual_1_full');
    const density1 = document.getElementById('actual_1_density');
    const hidden1 = document.getElementById('actual_1_density_hidden');
    
    if (empty1 && water1 && sand1 && full1 && density1) {
        const e1 = parseFloat(empty1.value);
        const w1 = parseFloat(water1.value);
        const s1 = parseFloat(sand1.value);
        const f1 = parseFloat(full1.value);
        
        console.log('Образец 1:', { empty: e1, water: w1, sand: s1, full: f1 });
        
        if (!isNaN(e1) && !isNaN(w1) && !isNaN(s1) && !isNaN(f1)) {
            // Формула: плотность = (масса песка - масса пустого) / ((масса с водой - масса пустого) - (масса полного - масса с песком))
            // Упрощенно: плотность = (s1 - e1) / ((w1 - e1) - (f1 - s1))
            const massSand = s1 - e1;
            const volumeWater = w1 - e1;
            const volumeSand = volumeWater - (f1 - s1);
            
            if (volumeSand > 0) {
                const actualDensity1 = massSand / volumeSand;
                const rounded1 = Math.round(actualDensity1 * 1000) / 1000;
                density1.value = rounded1;
                if (hidden1) hidden1.value = rounded1;
                console.log(`Истинная плотность 1: ${rounded1} г/см³`);
            }
        }
    }
    
    // Второй образец
    const empty2 = document.getElementById('actual_2_empty');
    const water2 = document.getElementById('actual_2_water');
    const sand2 = document.getElementById('actual_2_sand');
    const full2 = document.getElementById('actual_2_full');
    const density2 = document.getElementById('actual_2_density');
    const hidden2 = document.getElementById('actual_2_density_hidden');
    
    if (empty2 && water2 && sand2 && full2 && density2) {
        const e2 = parseFloat(empty2.value);
        const w2 = parseFloat(water2.value);
        const s2 = parseFloat(sand2.value);
        const f2 = parseFloat(full2.value);
        
        console.log('Образец 2:', { empty: e2, water: w2, sand: s2, full: f2 });
        
        if (!isNaN(e2) && !isNaN(w2) && !isNaN(s2) && !isNaN(f2)) {
            const massSand = s2 - e2;
            const volumeWater = w2 - e2;
            const volumeSand = volumeWater - (f2 - s2);
            
            if (volumeSand > 0) {
                const actualDensity2 = massSand / volumeSand;
                const rounded2 = Math.round(actualDensity2 * 1000) / 1000;
                density2.value = rounded2;
                if (hidden2) hidden2.value = rounded2;
                console.log(`Истинная плотность 2: ${rounded2} г/см³`);
            }
        }
    }
    
    // Среднее значение
    const average = document.getElementById('actual_average_density');
    const hiddenAvg = document.getElementById('actual_average_density_hidden');
    
    if (average && density1 && density2) {
        const d1 = parseFloat(density1.value);
        const d2 = parseFloat(density2.value);
        
        if (!isNaN(d1) && !isNaN(d2)) {
            const avg = (d1 + d2) / 2;
            const roundedAvg = Math.round(avg * 1000) / 1000;
            average.value = roundedAvg;
            if (hiddenAvg) hiddenAvg.value = roundedAvg;
            console.log(`Средняя истинная плотность: ${roundedAvg} г/см³`);
        } else if (!isNaN(d1)) {
            average.value = d1;
            if (hiddenAvg) hiddenAvg.value = d1;
        } else if (!isNaN(d2)) {
            average.value = d2;
            if (hiddenAvg) hiddenAvg.value = d2;
        }
    }
}

// Функция для расчета пустотности
function calculateEmptiness() {
    console.log('calculateEmptiness called');
    
    const bulkDensity = document.getElementById('bulk_average_density');
    const actualDensity = document.getElementById('actual_average_density');
    const emptiness = document.getElementById('emptiness');
    const hiddenEmptiness = document.getElementById('emptiness_hidden');
    
    if (bulkDensity && actualDensity && emptiness) {
        const bulk = parseFloat(bulkDensity.value);
        const actual = parseFloat(actualDensity.value);
        
        console.log('Для пустотности:', { bulk: bulk, actual: actual });
        
        if (!isNaN(bulk) && !isNaN(actual) && actual > 0) {
            // Формула: Пустотность = ((истинная - насыпная) / истинная) * 100
            const empt = ((actual - bulk) / actual) * 100;
            const rounded = Math.round(empt * 100) / 100;
            emptiness.value = rounded;
            if (hiddenEmptiness) hiddenEmptiness.value = rounded;
            console.log(`Пустотность: ${rounded}%`);
        }
    }
}

// Функция для расчета насыпной плотности
function calculateBulkDensity() {
    console.log('calculateBulkDensity called');
    
    // Первый образец
    const volume1 = document.getElementById('bulk_1_volume');
    const empty1 = document.getElementById('bulk_1_empty');
    const full1 = document.getElementById('bulk_1_full');
    const density1 = document.getElementById('bulk_1_density');
    const hidden1 = document.getElementById('bulk_1_density_hidden');
    
    if (volume1 && empty1 && full1 && density1) {
        const v1 = parseFloat(volume1.value);
        const e1 = parseFloat(empty1.value);
        const f1 = parseFloat(full1.value);
        
        if (!isNaN(v1) && !isNaN(e1) && !isNaN(f1) && v1 > 0) {
            const bulkDensity1 = (f1 - e1) / v1;
            const rounded1 = Math.round(bulkDensity1 * 1000) / 1000;
            density1.value = rounded1;
            if (hidden1) hidden1.value = rounded1;
            console.log(`Насыпная плотность 1: ${rounded1} г/см³`);
        }
    }
    
    // Второй образец
    const volume2 = document.getElementById('bulk_2_volume');
    const empty2 = document.getElementById('bulk_2_empty');
    const full2 = document.getElementById('bulk_2_full');
    const density2 = document.getElementById('bulk_2_density');
    const hidden2 = document.getElementById('bulk_2_density_hidden');
    
    if (volume2 && empty2 && full2 && density2) {
        const v2 = parseFloat(volume2.value);
        const e2 = parseFloat(empty2.value);
        const f2 = parseFloat(full2.value);
        
        if (!isNaN(v2) && !isNaN(e2) && !isNaN(f2) && v2 > 0) {
            const bulkDensity2 = (f2 - e2) / v2;
            const rounded2 = Math.round(bulkDensity2 * 1000) / 1000;
            density2.value = rounded2;
            if (hidden2) hidden2.value = rounded2;
            console.log(`Насыпная плотность 2: ${rounded2} г/см³`);
        }
    }
    
    // Среднее значение
    const average = document.getElementById('bulk_average_density');
    const hiddenAvg = document.getElementById('bulk_average_density_hidden');
    
    if (average && density1 && density2) {
        const d1 = parseFloat(density1.value);
        const d2 = parseFloat(density2.value);
        
        if (!isNaN(d1) && !isNaN(d2)) {
            const avg = (d1 + d2) / 2;
            const roundedAvg = Math.round(avg * 1000) / 1000;
            average.value = roundedAvg;
            if (hiddenAvg) hiddenAvg.value = roundedAvg;
            console.log(`Средняя насыпная плотность: ${roundedAvg} г/см³`);
            
            // После расчета насыпной плотности, пересчитываем пустотность
            calculateEmptiness();
        }
    }
}

// Добавляем обработчики событий
document.addEventListener('DOMContentLoaded', function() {
    console.log('Setting up density calculation handlers...');
    
    // Обработчики для истинной плотности
    const actualFields = [
        'actual_1_empty', 'actual_1_water', 'actual_1_sand', 'actual_1_full',
        'actual_2_empty', 'actual_2_water', 'actual_2_sand', 'actual_2_full'
    ];
    
    actualFields.forEach(id => {
        const field = document.getElementById(id);
        if (field) {
            field.addEventListener('input', function() {
                calculateActualDensity();
                calculateEmptiness();
            });
            field.addEventListener('change', function() {
                calculateActualDensity();
                calculateEmptiness();
            });
        }
    });
    
    // Обработчики для насыпной плотности
    const bulkFields = [
        'bulk_1_volume', 'bulk_1_empty', 'bulk_1_full',
        'bulk_2_volume', 'bulk_2_empty', 'bulk_2_full'
    ];
    
    bulkFields.forEach(id => {
        const field = document.getElementById(id);
        if (field) {
            field.addEventListener('input', function() {
                calculateBulkDensity();
                calculateEmptiness();
            });
            field.addEventListener('change', function() {
                calculateBulkDensity();
                calculateEmptiness();
            });
        }
    });
    
    // Запускаем расчеты при загрузке
    setTimeout(function() {
        calculateBulkDensity();
        calculateActualDensity();
        calculateEmptiness();
    }, 500);
});

// Экспортируем функции
window.calculateActualDensity = calculateActualDensity;
window.calculateBulkDensity = calculateBulkDensity;
window.calculateEmptiness = calculateEmptiness;
