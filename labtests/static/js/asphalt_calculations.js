// Функции для автоматических расчетов асфальтобетона

document.addEventListener('DOMContentLoaded', function() {
    console.log('Asphalt calculations script loaded');
    
    // Настраиваем обработчики событий для плотности
    setupDensityCalculations();
    
    // Настраиваем обработчики для гранулометрического состава
    setupPartitionCalculations();
    
    // Настраиваем обработчики для максимальной плотности
    setupMaxDensityCalculations();
    
    // Настраиваем обработчики для содержания вяжущего
    setupViscousCalculations();
    
    // Настраиваем обработчики для стекания вяжущего
    setupBinderCalculations();
});

// === РАСЧЕТЫ ПЛОТНОСТИ ===
function setupDensityCalculations() {
    for (let i = 1; i <= 3; i++) {
        // g1 (в воде) -> расчет g2-g1
        const waterInput = document.getElementById(`density_${i}_water`);
        const airAfterWaterInput = document.getElementById(`density_${i}_air_after_water`);
        
        if (waterInput) {
            waterInput.addEventListener('input', () => calculateDiffG2G1(i));
        }
        if (airAfterWaterInput) {
            airAfterWaterInput.addEventListener('input', () => calculateDiffG2G1(i));
        }
        
        // g (на воздухе) -> расчет плотности
        const airInput = document.getElementById(`density_${i}_air`);
        if (airInput) {
            airInput.addEventListener('input', () => calculateDensity(i));
        }
    }
}

function calculateDiffG2G1(index) {
    const g1 = parseFloat(document.getElementById(`density_${index}_water`).value) || 0;
    const g2 = parseFloat(document.getElementById(`density_${index}_air_after_water`).value) || 0;
    
    if (g1 && g2) {
        const diff = g2 - g1;
        document.getElementById(`density_${index}_diff_g2g1`).value = diff.toFixed(1);
        calculateDensity(index);
    }
}

function calculateDensity(index) {
    const g = parseFloat(document.getElementById(`density_${index}_air`).value) || 0;
    const diffG2G1 = parseFloat(document.getElementById(`density_${index}_diff_g2g1`).value) || 0;
    
    if (g && diffG2G1) {
        const density = (g / diffG2G1) * 0.997;
        document.getElementById(`density_${index}_density`).value = density.toFixed(3);
        calculateAverageDensity();
    }
}

function calculateAverageDensity() {
    const d1 = parseFloat(document.getElementById('density_1_density').value) || 0;
    const d2 = parseFloat(document.getElementById('density_2_density').value) || 0;
    const d3 = parseFloat(document.getElementById('density_3_density').value) || 0;
    
    let count = 0;
    let sum = 0;
    
    if (d1) { sum += d1; count++; }
    if (d2) { sum += d2; count++; }
    if (d3) { sum += d3; count++; }
    
    if (count >= 2) {
        // Проверяем разброс между образцами (не более 0.02)
        const values = [d1, d2, d3].filter(v => v > 0);
        let validPairs = [];
        
        for (let i = 0; i < values.length - 1; i++) {
            for (let j = i + 1; j < values.length; j++) {
                if (Math.abs(values[i] - values[j]) <= 0.02) {
                    validPairs.push((values[i] + values[j]) / 2);
                }
            }
        }
        
        if (validPairs.length > 0) {
            const avgDensity = validPairs[0];
            document.getElementById('average_density').value = avgDensity.toFixed(3);
            calculateVoidVolume();
        }
    }
}

function calculateVoidVolume() {
    const avgDensity = parseFloat(document.getElementById('average_density').value) || 0;
    const maxDensity = parseFloat(document.getElementById('max_density').value) || 0;
    
    if (avgDensity && maxDensity) {
        const voidVolume = (1 - avgDensity / maxDensity) * 100;
        document.getElementById('void_volume').value = voidVolume.toFixed(1);
    }
}

// === РАСЧЕТЫ ГРАНУЛОМЕТРИЧЕСКОГО СОСТАВА ===
function setupPartitionCalculations() {
    const fractions = ['31_5', '22_4', '16', '11_2', '8', '5_6', '4', '2', '0_125', '0_063'];
    
    fractions.forEach((fraction, index) => {
        const weightInput = document.getElementById(`partition_${fraction}_weight`);
        if (weightInput) {
            weightInput.addEventListener('input', () => calculatePartition(fraction, index, fractions));
        }
    });
}

function calculatePartition(fraction, index, fractions) {
    // Получаем общую массу
    let totalWeight = 0;
    fractions.forEach(f => {
        const weight = parseFloat(document.getElementById(`partition_${f}_weight`).value) || 0;
        totalWeight += weight;
    });
    
    if (totalWeight === 0) return;
    
    // Рассчитываем ЧО (частный остаток) и ПП (полный проход)
    let cumulativePass = 100;
    
    fractions.forEach((f, i) => {
        const weight = parseFloat(document.getElementById(`partition_${f}_weight`).value) || 0;
        const cho = (weight / totalWeight) * 100;
        
        // ЧО - частный остаток
        const choField = document.getElementById(`partition_${f}_cho`);
        if (choField) {
            choField.value = cho.toFixed(1);
        }
        
        // ПП - полный проход
        if (i === 0) {
            cumulativePass = 100 - cho;
        } else {
            const prevWeight = fractions.slice(0, i).reduce((sum, prevF) => {
                return sum + (parseFloat(document.getElementById(`partition_${prevF}_weight`).value) || 0);
            }, 0);
            const prevCho = (prevWeight / totalWeight) * 100;
            cumulativePass = 100 - prevCho - cho;
        }
        
        const ppField = document.getElementById(`partition_${f}_pp`);
        if (ppField) {
            ppField.value = cumulativePass.toFixed(1);
        }
    });
}

// === РАСЧЕТЫ МАКСИМАЛЬНОЙ ПЛОТНОСТИ ===
function setupMaxDensityCalculations() {
    const mixWeightInput = document.getElementById('max_mix_density_mix_weight');
    const afterVacuumInput = document.getElementById('max_mix_density_after_vacuum');
    const plateWeightInput = document.getElementById('max_mix_density_plate_weight');
    
    if (mixWeightInput) {
        mixWeightInput.addEventListener('input', calculateMaxDensity);
    }
    if (afterVacuumInput) {
        afterVacuumInput.addEventListener('input', calculateMaxDensity);
    }
    if (plateWeightInput) {
        plateWeightInput.addEventListener('input', calculateMaxDensity);
    }
}

function calculateMaxDensity() {
    const mixWeight = parseFloat(document.getElementById('max_mix_density_mix_weight').value) || 0;
    const afterVacuum = parseFloat(document.getElementById('max_mix_density_after_vacuum').value) || 0;
    const plateWeight = parseFloat(document.getElementById('max_mix_density_plate_weight').value) || 0;
    
    if (mixWeight && afterVacuum && plateWeight) {
        const maxDensity = mixWeight / (mixWeight - (afterVacuum - plateWeight)) * 0.997;
        document.getElementById('max_density').value = maxDensity.toFixed(3);
        calculateVoidVolume();
    }
}

// === РАСЧЕТЫ СОДЕРЖАНИЯ ВЯЖУЩЕГО ===
function setupViscousCalculations() {
    const tigleWeightInput = document.getElementById('viscous_tigle_weight');
    const mixTigleBeforeInput = document.getElementById('viscous_mix_tigle_before');
    const mixTigleAfterInput = document.getElementById('viscous_mix_tigle_after');
    
    if (tigleWeightInput) {
        tigleWeightInput.addEventListener('input', calculateBitumenContent);
    }
    if (mixTigleBeforeInput) {
        mixTigleBeforeInput.addEventListener('input', calculateBitumenContent);
    }
    if (mixTigleAfterInput) {
        mixTigleAfterInput.addEventListener('input', calculateBitumenContent);
    }
}

function calculateBitumenContent() {
    const tigleWeight = parseFloat(document.getElementById('viscous_tigle_weight').value) || 0;
    const mixTigleBefore = parseFloat(document.getElementById('viscous_mix_tigle_before').value) || 0;
    const mixTigleAfter = parseFloat(document.getElementById('viscous_mix_tigle_after').value) || 0;
    
    if (tigleWeight && mixTigleBefore && mixTigleAfter) {
        const mixWeight = mixTigleBefore - tigleWeight;
        const residueWeight = mixTigleAfter - tigleWeight;
        const bitumenWeight = mixWeight - residueWeight;
        const bitumenContent = (bitumenWeight / mixWeight) * 100;
        
        document.getElementById('viscous_bitumen_content').value = bitumenContent.toFixed(1);
    }
}

// === РАСЧЕТЫ СТЕКАНИЯ ВЯЖУЩЕГО ===
function setupBinderCalculations() {
    const emptyGlassInput = document.getElementById('binder_empty_glass');
    const fullGlassInput = document.getElementById('binder_full_glass');
    const glassAfterInput = document.getElementById('binder_glass_after');
    
    if (emptyGlassInput) {
        emptyGlassInput.addEventListener('input', calculateBinderTrickling);
    }
    if (fullGlassInput) {
        fullGlassInput.addEventListener('input', calculateBinderTrickling);
    }
    if (glassAfterInput) {
        glassAfterInput.addEventListener('input', calculateBinderTrickling);
    }
}

function calculateBinderTrickling() {
    const emptyGlass = parseFloat(document.getElementById('binder_empty_glass').value) || 0;
    const fullGlass = parseFloat(document.getElementById('binder_full_glass').value) || 0;
    const glassAfter = parseFloat(document.getElementById('binder_glass_after').value) || 0;
    
    if (emptyGlass && fullGlass && glassAfter) {
        const mixWeight = fullGlass - emptyGlass;
        const trickling = glassAfter - emptyGlass;
        const tricklingPercent = (trickling / mixWeight) * 100;
        
        document.getElementById('binder_trickling').value = tricklingPercent.toFixed(2);
    }
}

// === ПРОВЕРКА ОТКЛОНЕНИЙ ===
function setupVarianceCheck() {
    const fractions = ['31_5', '22_4', '16', '11_2', '8', '5_6', '4', '2', '0_125', '0_063'];
    
    fractions.forEach(fraction => {
        const receiptInput = document.getElementById(`partition_${fraction}_receipt`);
        const ppInput = document.getElementById(`partition_${fraction}_pp`);
        
        if (receiptInput && ppInput) {
            receiptInput.addEventListener('input', () => checkVariance(fraction));
            // Также проверяем при изменении ПП
            const observer = new MutationObserver(() => checkVariance(fraction));
            observer.observe(ppInput, { attributes: true, attributeFilter: ['value'] });
        }
    });
}

function checkVariance(fraction) {
    const receiptValue = parseFloat(document.getElementById(`partition_${fraction}_receipt`).value) || 0;
    const ppValue = parseFloat(document.getElementById(`partition_${fraction}_pp`).value) || 0;
    const varianceInput = document.querySelector(`input[name="partition_${fraction}_variance"]`);
    
    if (varianceInput && varianceInput.value && receiptValue && ppValue) {
        const variance = parseFloat(varianceInput.value);
        const diff = Math.abs(ppValue - receiptValue);
        
        const ppField = document.getElementById(`partition_${fraction}_pp`);
        if (diff > variance) {
            ppField.classList.add('input-alert');
        } else {
            ppField.classList.remove('input-alert');
        }
    }
}

// Вызываем настройку проверки отклонений при загрузке
document.addEventListener('DOMContentLoaded', function() {
    setupVarianceCheck();
});
