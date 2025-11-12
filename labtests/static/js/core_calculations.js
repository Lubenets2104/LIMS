/**
 * Расчеты для кернов из асфальтобетона
 * Автоматические вычисления для формы испытаний кернов
 */

// Ждем загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    console.log('Инициализация расчетов для кернов');
    
    // Инициализация слушателей событий
    initLayer1Calculations();
    
    // Выполняем первоначальный расчет при загрузке
    performCalculations();
});

// Инициализация расчетов для Слоя 1
function initLayer1Calculations() {
    // Слушатели для образца 1
    const sample1Fields = ['layer1_sample1_g', 'layer1_sample1_g1', 'layer1_sample1_g2'];
    sample1Fields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', calculateSample1);
            field.addEventListener('change', calculateSample1);
        }
    });
    
    // Слушатели для образца 2
    const sample2Fields = ['layer1_sample2_g', 'layer1_sample2_g1', 'layer1_sample2_g2'];
    sample2Fields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', calculateSample2);
            field.addEventListener('change', calculateSample2);
        }
    });
    
    // Слушатель для max_density
    const maxDensityField = document.getElementById('layer1_max_density');
    if (maxDensityField) {
        maxDensityField.addEventListener('input', calculateVoidVolume);
        maxDensityField.addEventListener('change', calculateVoidVolume);
    }
}

// Расчет для образца 1
function calculateSample1() {
    console.log('Расчет для образца 1');
    
    const g = parseFloat(document.getElementById('layer1_sample1_g').value) || 0;
    const g1 = parseFloat(document.getElementById('layer1_sample1_g1').value) || 0;
    const g2 = parseFloat(document.getElementById('layer1_sample1_g2').value) || 0;
    
    // Вычисляем g2 - g1
    const g2g1Field = document.getElementById('layer1_sample1_g2g1');
    if (g2g1Field) {
        const g2g1 = g2 - g1;
        g2g1Field.value = g2g1 > 0 ? g2g1.toFixed(1) : '';
        
        // Вычисляем плотность: ρ = g / (g2 - g1)
        const densityField = document.getElementById('layer1_sample1_density');
        if (densityField && g > 0 && g2g1 > 0) {
            const density = g / g2g1;
            densityField.value = density.toFixed(3);
        } else if (densityField) {
            densityField.value = '';
        }
    }
    
    // Пересчитываем средние значения
    calculateAverageDensity();
}

// Расчет для образца 2
function calculateSample2() {
    console.log('Расчет для образца 2');
    
    const g = parseFloat(document.getElementById('layer1_sample2_g').value) || 0;
    const g1 = parseFloat(document.getElementById('layer1_sample2_g1').value) || 0;
    const g2 = parseFloat(document.getElementById('layer1_sample2_g2').value) || 0;
    
    // Вычисляем g2 - g1
    const g2g1Field = document.getElementById('layer1_sample2_g2g1');
    if (g2g1Field) {
        const g2g1 = g2 - g1;
        g2g1Field.value = g2g1 > 0 ? g2g1.toFixed(1) : '';
        
        // Вычисляем плотность: ρ = g / (g2 - g1)
        const densityField = document.getElementById('layer1_sample2_density');
        if (densityField && g > 0 && g2g1 > 0) {
            const density = g / g2g1;
            densityField.value = density.toFixed(3);
        } else if (densityField) {
            densityField.value = '';
        }
    }
    
    // Пересчитываем средние значения
    calculateAverageDensity();
}

// Расчет средней плотности
function calculateAverageDensity() {
    console.log('Расчет средней плотности');
    
    const density1 = parseFloat(document.getElementById('layer1_sample1_density').value) || 0;
    const density2 = parseFloat(document.getElementById('layer1_sample2_density').value) || 0;
    
    const avgDensityField = document.getElementById('layer1_average_density');
    if (avgDensityField) {
        let avgDensity = 0;
        let count = 0;
        
        if (density1 > 0) {
            avgDensity += density1;
            count++;
        }
        if (density2 > 0) {
            avgDensity += density2;
            count++;
        }
        
        if (count > 0) {
            avgDensity = avgDensity / count;
            avgDensityField.value = avgDensity.toFixed(3);
        } else {
            avgDensityField.value = '';
        }
    }
    
    // Пересчитываем пустотность
    calculateVoidVolume();
}

// Расчет пустотности
function calculateVoidVolume() {
    console.log('Расчет пустотности');
    
    const avgDensity = parseFloat(document.getElementById('layer1_average_density').value) || 0;
    const maxDensity = parseFloat(document.getElementById('layer1_max_density').value) || 0;
    
    const voidField = document.getElementById('layer1_void_volume');
    if (voidField && avgDensity > 0 && maxDensity > 0) {
        // Формула: Пустоты = (1 - ρср/ρmax) * 100
        const voidVolume = (1 - avgDensity / maxDensity) * 100;
        voidField.value = voidVolume.toFixed(1);
        
        // Подсветка, если пустотность выходит за пределы нормы
        // Обычно норма 3-5% для покрытия, 4-10% для основания
        if (voidVolume < 3 || voidVolume > 10) {
            voidField.style.backgroundColor = '#ffcccc';
        } else {
            voidField.style.backgroundColor = '#e9ecef';
        }
    } else {
        voidField.value = '';
        voidField.style.backgroundColor = '#e9ecef';
    }
}

// Выполнение всех расчетов
function performCalculations() {
    calculateSample1();
    calculateSample2();
    calculateAverageDensity();
    calculateVoidVolume();
}

// Функция для проверки заполненности обязательных полей
function checkRequiredFields() {
    const requiredFields = [
        'layer1_type',
        'layer1_mix_name',
        'layer1_sample1_g',
        'layer1_sample1_g1',
        'layer1_sample1_g2',
        'layer1_sample2_g',
        'layer1_sample2_g1',
        'layer1_sample2_g2',
        'layer1_max_density'
    ];
    
    let allFilled = true;
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field && !field.value) {
            allFilled = false;
            field.style.borderColor = '#ff0000';
        } else if (field) {
            field.style.borderColor = '#ddd';
        }
    });
    
    return allFilled;
}

// Добавляем проверку при отправке формы
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('core-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!checkRequiredFields()) {
                e.preventDefault();
                alert('Пожалуйста, заполните все обязательные поля');
            }
        });
    }
});

console.log('core_calculations.js загружен успешно');
