// Расчеты для асфальтобетона

// Функция для безопасного парсинга чисел
function safeParseFloat(value) {
    if (!value || value === '') return 0;
    // Заменяем запятую на точку
    const normalizedValue = String(value).replace(',', '.');
    const parsed = parseFloat(normalizedValue);
    return isNaN(parsed) ? 0 : parsed;
}

// Функция для безопасного округления
function safeRound(value, decimals = 2) {
    if (isNaN(value) || !isFinite(value)) return '';
    return Math.round(value * Math.pow(10, decimals)) / Math.pow(10, decimals);
}

// Функция для обработки текстовых полей с числами
function setupTextNumberInputHandlers(input) {
    if (!input) return;
    
    // Не очищаем существующие значения
    // Просто добавляем обработчики для будущего ввода
    
    // Обработка ввода
    input.addEventListener('input', function(e) {
        let value = this.value;
        
        // Заменяем запятую на точку
        value = value.replace(',', '.');
        
        // Удаляем все символы, кроме цифр и точки
        value = value.replace(/[^0-9.]/g, '');
        
        // Оставляем только одну точку
        const parts = value.split('.');
        if (parts.length > 2) {
            value = parts[0] + '.' + parts.slice(1).join('');
        }
        
        // Обновляем значение, только если оно изменилось
        if (this.value !== value) {
            this.value = value;
        }
    });
    
    // Обработка вставки из буфера обмена
    input.addEventListener('paste', function(e) {
        e.preventDefault();
        const pastedText = (e.clipboardData || window.clipboardData).getData('text');
        const normalizedText = pastedText.replace(',', '.').replace(/[^0-9.]/g, '');
        
        this.value = normalizedText;
        this.dispatchEvent(new Event('input', { bubbles: true }));
    });
}

// Функция для обработки полей type="number"
function setupNumberInputHandlers(input) {
    if (!input || input.type !== 'number') return;
    
    // Сохраняем последнее валидное значение
    let lastValidValue = input.value;
    
    // Обработка ввода с клавиатуры
    input.addEventListener('keydown', function(e) {
        // Если нажата запятая
        if (e.key === ',') {
            e.preventDefault();
            
            const value = this.value;
            const cursorPos = this.selectionStart;
            
            // Проверяем, есть ли уже точка в значении
            if (!value.includes('.')) {
                // Вставляем точку в текущую позицию курсора
                const newValue = value.slice(0, cursorPos) + '.' + value.slice(cursorPos);
                this.value = newValue;
                // Устанавливаем курсор после точки
                this.setSelectionRange(cursorPos + 1, cursorPos + 1);
                // Запускаем событие input для активации расчетов
                this.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
    });
    
    // Обработка вставки из буфера обмена
    input.addEventListener('paste', function(e) {
        e.preventDefault();
        const pastedText = (e.clipboardData || window.clipboardData).getData('text');
        const normalizedText = pastedText.replace(',', '.');
        
        // Проверяем, что это валидное число
        if (!isNaN(parseFloat(normalizedText))) {
            this.value = normalizedText;
            this.dispatchEvent(new Event('input', { bubbles: true }));
        }
    });
    
    // Валидация при потере фокуса
    input.addEventListener('blur', function() {
        if (this.value && isNaN(parseFloat(this.value))) {
            this.value = lastValidValue;
        } else {
            lastValidValue = this.value;
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Asphalt calculations loaded');
    
    // Задержка инициализации, чтобы дать время загрузиться значениям
    setTimeout(function() {
        // Применяем обработчики ко всем числовым полям
        const numberInputs = document.querySelectorAll('input[type="number"], input.number-input');
        numberInputs.forEach(input => {
            if (input.classList.contains('number-input')) {
                setupTextNumberInputHandlers(input);
            } else {
                setupNumberInputHandlers(input);
            }
        });
        
        // Инициализация обработчиков для измерений плотности
        for (let i = 1; i <= 3; i++) {
            setupDensityCalculations(i);
        }
        
        // Инициализация расчетов максимальной плотности
        setupMaxDensityCalculations();
        
        // Инициализация расчетов содержания вяжущего
        setupViscousCalculations();
        
        // Инициализация расчетов стекания вяжущего
        setupBinderCalculations();
        
        // Инициализация расчетов гранулометрического состава
        setupPartitionCalculations();
        
        console.log('All calculations initialized');
    }, 500); // Задержка 500мс
});

// === РАСЧЕТЫ ПЛОТНОСТИ ===
function setupDensityCalculations(index) {
    const waterInput = document.getElementById(`density_${index}_water`);
    const airAfterWaterInput = document.getElementById(`density_${index}_air_after_water`);
    const airInput = document.getElementById(`density_${index}_air`);
    
    if (waterInput && airAfterWaterInput) {
        waterInput.addEventListener('input', () => calculateG2G1(index));
        airAfterWaterInput.addEventListener('input', () => calculateG2G1(index));
    }
    
    if (airInput) {
        airInput.addEventListener('input', () => calculateDensity(index));
    }
}

function calculateG2G1(index) {
    const g1 = safeParseFloat(document.getElementById(`density_${index}_water`).value);
    const g2 = safeParseFloat(document.getElementById(`density_${index}_air_after_water`).value);
    const diffField = document.getElementById(`density_${index}_diff_g2g1`);
    
    if (g1 > 0 && g2 > 0) {
        const diff = safeRound(g2 - g1, 2);
        diffField.value = diff;
        calculateDensity(index);
    } else {
        diffField.value = '';
    }
}

function calculateDensity(index) {
    const g = safeParseFloat(document.getElementById(`density_${index}_air`).value);
    const g2g1 = safeParseFloat(document.getElementById(`density_${index}_diff_g2g1`).value);
    const densityField = document.getElementById(`density_${index}_density`);
    
    if (g > 0 && g2g1 > 0) {
        const density = safeRound((g / g2g1) * 0.997, 3);
        densityField.value = density;
        calculateAverageDensity();
    } else {
        densityField.value = '';
    }
}

function calculateAverageDensity() {
    const d1 = safeParseFloat(document.getElementById('density_1_density').value);
    const d2 = safeParseFloat(document.getElementById('density_2_density').value);
    const d3 = safeParseFloat(document.getElementById('density_3_density').value);
    const avgField = document.getElementById('average_density');
    
    const densities = [d1, d2, d3].filter(d => d > 0);
    
    if (densities.length >= 2) {
        // Проверка на расхождение
        let validPairs = [];
        
        if (d1 > 0 && d2 > 0 && Math.abs(d1 - d2) <= 0.02) {
            validPairs.push([d1, d2]);
        }
        if (d2 > 0 && d3 > 0 && Math.abs(d2 - d3) <= 0.02) {
            validPairs.push([d2, d3]);
        }
        if (d1 > 0 && d3 > 0 && Math.abs(d1 - d3) <= 0.02) {
            validPairs.push([d1, d3]);
        }
        
        if (validPairs.length > 0) {
            // Берем первую подходящую пару
            const avg = safeRound((validPairs[0][0] + validPairs[0][1]) / 2, 3);
            avgField.value = avg;
            
            // Убираем предупреждения
            document.getElementById('density_1_density').classList.remove('input-alert');
            document.getElementById('density_2_density').classList.remove('input-alert');
            document.getElementById('density_3_density').classList.remove('input-alert');
            
            calculateVoidVolume();
        } else if (densities.length === 3) {
            // Все три значения есть, но расхождение больше 0.02
            document.getElementById('density_1_density').classList.add('input-alert');
            document.getElementById('density_2_density').classList.add('input-alert');
            document.getElementById('density_3_density').classList.add('input-alert');
            avgField.value = '';
        }
    } else {
        avgField.value = '';
    }
}

// === РАСЧЕТ МАКСИМАЛЬНОЙ ПЛОТНОСТИ ===
function setupMaxDensityCalculations() {
    const mixWeightInput = document.getElementById('max_mix_density_mix_weight');
    const afterVacuumInput = document.getElementById('max_mix_density_after_vacuum');
    const plateWeightInput = document.getElementById('max_mix_density_plate_weight');
    
    if (mixWeightInput) mixWeightInput.addEventListener('input', calculateMaxDensity);
    if (afterVacuumInput) afterVacuumInput.addEventListener('input', calculateMaxDensity);
    if (plateWeightInput) plateWeightInput.addEventListener('input', calculateMaxDensity);
}

function calculateMaxDensity() {
    const mw = safeParseFloat(document.getElementById('max_mix_density_mix_weight').value);
    const avw = safeParseFloat(document.getElementById('max_mix_density_after_vacuum').value);
    const pw = safeParseFloat(document.getElementById('max_mix_density_plate_weight').value);
    const maxDensityField = document.getElementById('max_density');
    
    if (mw > 0 && avw > 0 && pw > 0) {
        const denominator = mw - (avw - pw);
        if (denominator > 0) {
            const maxDensity = safeRound((mw / denominator) * 0.997, 3);
            maxDensityField.value = maxDensity;
            calculateVoidVolume();
        } else {
            maxDensityField.value = '';
        }
    } else {
        maxDensityField.value = '';
    }
}

// === РАСЧЕТ ПУСТОТНОСТИ ===
function calculateVoidVolume() {
    const avgDensity = safeParseFloat(document.getElementById('average_density').value);
    const maxDensity = safeParseFloat(document.getElementById('max_density').value);
    const voidField = document.getElementById('void_volume');
    
    if (avgDensity > 0 && maxDensity > 0) {
        const voidVolume = safeRound((1 - avgDensity / maxDensity) * 100, 1);
        voidField.value = voidVolume;
        checkVoidVolumeVariance();
    } else {
        voidField.value = '';
    }
}

function checkVoidVolumeVariance() {
    const voidField = document.getElementById('void_volume');
    const receiptField = document.getElementById('void_volume_receipt');
    const varianceField = document.getElementById('void_volume_variance');
    const minField = document.getElementById('void_volume_min');
    
    if (!voidField || !receiptField) return;
    
    const voidVolume = safeParseFloat(voidField.value);
    const receipt = safeParseFloat(receiptField.value);
    const variance = varianceField ? safeParseFloat(varianceField.value) : 1.2;
    const min = minField ? safeParseFloat(minField.value) : 2.5;
    
    if (voidVolume > 0 && receipt > 0) {
        const diff = Math.abs(voidVolume - receipt);
        if (diff > variance || voidVolume < min) {
            voidField.classList.add('input-alert');
        } else {
            voidField.classList.remove('input-alert');
        }
    } else {
        voidField.classList.remove('input-alert');
    }
}

// === СОДЕРЖАНИЕ ВЯЖУЩЕГО ===
function setupViscousCalculations() {
    const tigleWeightInput = document.getElementById('viscous_tigle_weight');
    const beforeInput = document.getElementById('viscous_mix_tigle_before');
    const afterInput = document.getElementById('viscous_mix_tigle_after');
    
    if (tigleWeightInput) tigleWeightInput.addEventListener('input', calculateBitumenContent);
    if (beforeInput) beforeInput.addEventListener('input', calculateBitumenContent);
    if (afterInput) afterInput.addEventListener('input', calculateBitumenContent);
}

function calculateBitumenContent() {
    const tw = safeParseFloat(document.getElementById('viscous_tigle_weight').value);
    const mtb = safeParseFloat(document.getElementById('viscous_mix_tigle_before').value);
    const mta = safeParseFloat(document.getElementById('viscous_mix_tigle_after').value);
    const contentField = document.getElementById('viscous_bitumen_content');
    
    if (tw > 0 && mtb > tw && mta > 0) {
        const denominator = mtb - tw;
        if (denominator > 0) {
            const content = safeRound(((mtb - tw) - (mta - tw)) / denominator * 100, 1);
            contentField.value = content;
            checkBitumenVariance();
            // После расчета содержания битума пересчитываем гранулометрический состав
            calculatePartitionCompounds();
        } else {
            contentField.value = '';
        }
    } else {
        contentField.value = '';
    }
}

function checkBitumenVariance() {
    const contentField = document.getElementById('viscous_bitumen_content');
    const receiptField = document.getElementById('viscous_bitumen_receipt');
    const varianceField = document.getElementById('viscous_bitumen_variance');
    
    if (!contentField || !receiptField) return;
    
    const content = safeParseFloat(contentField.value);
    const receipt = safeParseFloat(receiptField.value);
    const variance = varianceField ? safeParseFloat(varianceField.value) : 0.4;
    
    if (content > 0 && receipt > 0) {
        const diff = Math.abs(content - receipt);
        if (diff > variance) {
            contentField.classList.add('input-alert');
        } else {
            contentField.classList.remove('input-alert');
        }
    } else {
        contentField.classList.remove('input-alert');
    }
}

// === СТЕКАНИЕ ВЯЖУЩЕГО ===
function setupBinderCalculations() {
    const emptyInput = document.getElementById('binder_empty_glass');
    const fullInput = document.getElementById('binder_full_glass');
    const afterInput = document.getElementById('binder_glass_after');
    
    if (emptyInput) emptyInput.addEventListener('input', calculateBinderTrickling);
    if (fullInput) fullInput.addEventListener('input', calculateBinderTrickling);
    if (afterInput) afterInput.addEventListener('input', calculateBinderTrickling);
}

function calculateBinderTrickling() {
    const egw = safeParseFloat(document.getElementById('binder_empty_glass').value);
    const fgw = safeParseFloat(document.getElementById('binder_full_glass').value);
    const gwa = safeParseFloat(document.getElementById('binder_glass_after').value);
    const tricklingField = document.getElementById('binder_trickling');
    
    if (egw >= 0 && fgw > egw && gwa >= egw) {
        const denominator = fgw - egw;
        if (denominator > 0) {
            const trickling = safeRound((gwa - egw) / denominator * 100, 2);
            tricklingField.value = trickling;
            
            const maxTrickling = safeParseFloat(document.getElementById('binder_max_trickling').value) || 0.2;
            if (trickling > maxTrickling) {
                tricklingField.classList.add('input-alert');
            } else {
                tricklingField.classList.remove('input-alert');
            }
        } else {
            tricklingField.value = '';
        }
    } else {
        tricklingField.value = '';
    }
}

// === ГРАНУЛОМЕТРИЧЕСКИЙ СОСТАВ ===
function setupPartitionCalculations() {
    const fractions = ['31_5', '22_4', '16', '11_2', '8', '5_6', '4', '2', '0_125', '0_063'];
    
    fractions.forEach((fraction, index) => {
        const weightInput = document.getElementById(`partition_${fraction}_weight`);
        const receiptInput = document.getElementById(`partition_${fraction}_receipt`);
        
        if (weightInput) {
            weightInput.addEventListener('input', () => {
                calculatePartitionCompound(fraction, index);
            });
        }
        
        if (receiptInput) {
            receiptInput.addEventListener('input', () => checkPartitionVariance(fraction));
        }
    });
    
    // Также пересчитываем при изменении веса после выжигания
    const afterInput = document.getElementById('viscous_mix_tigle_after');
    if (afterInput) {
        afterInput.addEventListener('input', calculatePartitionCompounds);
    }
}

function calculatePartitionCompounds() {
    const fractions = ['31_5', '22_4', '16', '11_2', '8', '5_6', '4', '2', '0_125', '0_063'];
    fractions.forEach((fraction, index) => {
        calculatePartitionCompound(fraction, index);
    });
}

function calculatePartitionCompound(fraction, index) {
    const weight = safeParseFloat(document.getElementById(`partition_${fraction}_weight`).value);
    const tw = safeParseFloat(document.getElementById('viscous_tigle_weight').value);
    const mta = safeParseFloat(document.getElementById('viscous_mix_tigle_after').value);
    
    const choField = document.getElementById(`partition_${fraction}_cho`);
    const ppField = document.getElementById(`partition_${fraction}_pp`);
    
    if (weight > 0 && tw > 0 && mta > tw) {
        const denominator = mta - tw;
        if (denominator > 0) {
            const cho = safeRound(weight / denominator * 100, 1);
            choField.value = cho;
            
            // Расчет ПП (полного прохода)
            if (index === 0) {
                // Для первой фракции ПП = 100 - ЧО
                const pp = safeRound(100 - cho, 1);
                ppField.value = pp;
            } else {
                // Для остальных фракций ПП = ПП_предыдущей - ЧО_текущей
                const fractions = ['31_5', '22_4', '16', '11_2', '8', '5_6', '4', '2', '0_125', '0_063'];
                const prevFraction = fractions[index - 1];
                const prevPP = safeParseFloat(document.getElementById(`partition_${prevFraction}_pp`).value);
                
                if (prevPP > 0) {
                    const pp = safeRound(prevPP - cho, 1);
                    ppField.value = pp;
                } else {
                    ppField.value = '';
                }
            }
            
            // Пересчитываем все последующие фракции
            if (index < fractions.length - 1) {
                for (let i = index + 1; i < fractions.length; i++) {
                    calculatePartitionCompound(fractions[i], i);
                }
            }
            
            checkPartitionVariance(fraction);
        } else {
            choField.value = '';
            ppField.value = '';
        }
    } else {
        choField.value = '';
        ppField.value = '';
    }
}

function checkPartitionVariance(fraction) {
    const pp = safeParseFloat(document.getElementById(`partition_${fraction}_pp`).value);
    const receipt = safeParseFloat(document.getElementById(`partition_${fraction}_receipt`).value);
    const varianceInput = document.getElementById(`partition_${fraction}_variance`);
    const variance = varianceInput ? safeParseFloat(varianceInput.value) : 0;
    const ppField = document.getElementById(`partition_${fraction}_pp`);
    
    if (pp > 0 && receipt > 0 && variance > 0) {
        const diff = Math.abs(pp - receipt);
        if (diff > variance) {
            ppField.classList.add('input-alert');
        } else {
            ppField.classList.remove('input-alert');
        }
    } else {
        ppField.classList.remove('input-alert');
    }
}

// Добавляем обработчики для проверки отклонений при изменении согласованных составов
document.addEventListener('DOMContentLoaded', function() {
    const voidReceipt = document.getElementById('void_volume_receipt');
    const bitumenReceipt = document.getElementById('viscous_bitumen_receipt');
    
    if (voidReceipt) voidReceipt.addEventListener('input', checkVoidVolumeVariance);
    if (bitumenReceipt) bitumenReceipt.addEventListener('input', checkBitumenVariance);
});

console.log('Asphalt calculations script loaded successfully');
