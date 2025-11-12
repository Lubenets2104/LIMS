// JavaScript для автоматических расчетов листа измерений кернов из асфальтобетона

document.addEventListener('DOMContentLoaded', function() {
    console.log('Core calculations.js загружен');
    
    // Функция для безопасного парсинга чисел
    function safeParseFloat(value) {
        if (!value || value === '') return null;
        // Заменяем запятую на точку
        value = value.toString().replace(',', '.');
        const parsed = parseFloat(value);
        return isNaN(parsed) ? null : parsed;
    }
    
    // Функция для безопасного вывода числа
    function safeOutput(value, decimals = 3) {
        if (value === null || value === undefined || isNaN(value)) return '';
        return value.toFixed(decimals);
    }
    
    // Расчет g2-g1 и плотности для образца
    function calculateSampleDensity(sampleNum, layerNum) {
        const prefix = `layer${layerNum}_sample${sampleNum}`;
        
        const g = safeParseFloat(document.getElementById(`${prefix}_g`)?.value);
        const g1 = safeParseFloat(document.getElementById(`${prefix}_g1`)?.value);
        const g2 = safeParseFloat(document.getElementById(`${prefix}_g2`)?.value);
        
        // Расчет g2-g1
        const g2g1Field = document.getElementById(`${prefix}_g2g1`);
        if (g2g1Field) {
            if (g2 !== null && g1 !== null) {
                const g2g1 = g2 - g1;
                g2g1Field.value = safeOutput(g2g1, 1);
                
                // Расчет плотности: ρ = g / (g2-g1)
                const densityField = document.getElementById(`${prefix}_density`);
                if (densityField && g !== null && g2g1 > 0) {
                    const density = g / g2g1;
                    densityField.value = safeOutput(density, 3);
                }
            } else {
                g2g1Field.value = '';
                document.getElementById(`${prefix}_density`).value = '';
            }
        }
    }
    
    // Расчет средней плотности для слоя
    function calculateAverageDensity(layerNum) {
        const density1 = safeParseFloat(document.getElementById(`layer${layerNum}_sample1_density`)?.value);
        const density2 = safeParseFloat(document.getElementById(`layer${layerNum}_sample2_density`)?.value);
        
        const avgField = document.getElementById(`layer${layerNum}_average_density`);
        if (avgField) {
            const validDensities = [density1, density2].filter(d => d !== null);
            
            if (validDensities.length > 0) {
                const avg = validDensities.reduce((sum, d) => sum + d, 0) / validDensities.length;
                avgField.value = safeOutput(avg, 3);
                
                // Расчет пустотности если есть максимальная плотность
                calculateVoidVolume(layerNum);
            } else {
                avgField.value = '';
            }
        }
    }
    
    // Расчет пустотности
    function calculateVoidVolume(layerNum) {
        const avgDensity = safeParseFloat(document.getElementById(`layer${layerNum}_average_density`)?.value);
        const maxDensity = safeParseFloat(document.getElementById(`layer${layerNum}_max_density`)?.value);
        
        const voidField = document.getElementById(`layer${layerNum}_void_volume`);
        if (voidField && avgDensity !== null && maxDensity !== null && maxDensity > 0) {
            const voidVolume = ((maxDensity - avgDensity) / maxDensity) * 100;
            voidField.value = safeOutput(voidVolume, 1);
        } else if (voidField) {
            voidField.value = '';
        }
    }
    
    // Обработчики событий для слоя 1
    const layer1Fields = [
        'layer1_sample1_g', 'layer1_sample1_g1', 'layer1_sample1_g2',
        'layer1_sample2_g', 'layer1_sample2_g1', 'layer1_sample2_g2',
        'layer1_max_density'
    ];
    
    layer1Fields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', function() {
                // Определяем номер образца из ID поля
                if (fieldId.includes('sample1')) {
                    calculateSampleDensity(1, 1);
                } else if (fieldId.includes('sample2')) {
                    calculateSampleDensity(2, 1);
                }
                
                // Пересчитываем среднюю плотность
                calculateAverageDensity(1);
            });
        }
    });
    
    // Дополнительный обработчик для максимальной плотности
    const maxDensityField = document.getElementById('layer1_max_density');
    if (maxDensityField) {
        maxDensityField.addEventListener('input', function() {
            calculateVoidVolume(1);
        });
    }
    
    // Начальный расчет при загрузке страницы
    calculateSampleDensity(1, 1);
    calculateSampleDensity(2, 1);
    calculateAverageDensity(1);
    
    console.log('Обработчики для расчетов кернов установлены');
});
