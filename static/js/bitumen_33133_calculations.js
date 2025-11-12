/**
 * JavaScript для расчетов в листе измерений битума по ГОСТ 33133-2014
 */

// Маркер загрузки скрипта
window.bitumenScriptLoaded = true;

document.addEventListener('DOMContentLoaded', function() {
    console.log('Инициализация расчетов для битума ГОСТ 33133-2014');
    
    // === ФУНКЦИЯ ДЛЯ ПОКАЗА/СКРЫТИЯ ПОДСКАЗОК ===
    window.toggleHelp = function(helpId) {
        const helpDiv = document.getElementById(helpId);
        if (helpDiv) {
            helpDiv.style.display = helpDiv.style.display === 'none' ? 'block' : 'none';
        }
    }
    
    // === ПРОВЕРКА ГЛУБИНЫ ПРОНИКАНИЯ ИГЛЫ ===
    function validateNeedleDeep() {
        const value = parseFloat(document.getElementById('needle_deep')?.value) || 0;
        const min = parseFloat(document.getElementById('needle_deep_min')?.value) || 131;
        const max = parseFloat(document.getElementById('needle_deep_max')?.value) || 200;
        const field = document.getElementById('needle_deep');
        
        if (field && value > 0) {
            if (value < min || value > max) {
                field.classList.add('input-alert');
            } else {
                field.classList.remove('input-alert');
            }
        }
    }
    
    // === ПРОВЕРКА ТЕМПЕРАТУРЫ РАЗМЯГЧЕНИЯ ===
    function validateSofteningTemperature() {
        const value = parseFloat(document.getElementById('softening_temperature')?.value) || 0;
        const min = parseFloat(document.getElementById('softening_temperature_min')?.value) || 42;
        const field = document.getElementById('softening_temperature');
        
        if (field && value > 0) {
            if (value < min) {
                field.classList.add('input-alert');
            } else {
                field.classList.remove('input-alert');
            }
        }
    }
    
    // === ПРОВЕРКА РАСТЯЖИМОСТИ ===
    function validateExtensibility() {
        const value = parseFloat(document.getElementById('extensibility')?.value) || 0;
        const min = parseFloat(document.getElementById('extensibility_min')?.value) || 6;
        const field = document.getElementById('extensibility');
        
        if (field && value > 0) {
            if (value < min) {
                field.classList.add('input-alert');
            } else {
                field.classList.remove('input-alert');
            }
        }
    }
    
    // === ПРОВЕРКА ТЕМПЕРАТУРЫ ХРУПКОСТИ ===
    function validateFragilityTemperature() {
        const value = parseFloat(document.getElementById('fragility_temperature')?.value) || 0;
        const max = parseFloat(document.getElementById('fragility_temperature_max')?.value) || -21;
        const field = document.getElementById('fragility_temperature');
        
        if (field && value !== 0) {
            if (value > max) {
                field.classList.add('input-alert');
            } else {
                field.classList.remove('input-alert');
            }
        }
    }
    
    // === ПРОВЕРКА ТЕМПЕРАТУРЫ ВСПЫШКИ ===
    function validateFlashTemperature() {
        const value = parseFloat(document.getElementById('flash_temperature')?.value) || 0;
        const min = parseFloat(document.getElementById('flash_temperature_min')?.value) || 220;
        const field = document.getElementById('flash_temperature');
        
        if (field && value > 0) {
            if (value < min) {
                field.classList.add('input-alert');
            } else {
                field.classList.remove('input-alert');
            }
        }
    }
    
    // === РАСЧЕТ ИЗМЕНЕНИЯ МАССЫ ДЛЯ КОНТЕЙНЕРА А (ГОСТ 33140) ===
    function calculateContainerA() {
        const m_st = parseFloat(document.getElementById('container_a_weight')?.value) || 0;
        const m_do = parseFloat(document.getElementById('container_a_bitumen_before')?.value) || 0;
        const m_posle = parseFloat(document.getElementById('container_a_bitumen_after')?.value) || 0;
        
        if (m_st > 0 && m_do > m_st && m_posle > 0) {
            // Формула: Δm = (m_до - m_после) / (m_до - m_ст) × 100%
            const result = ((m_do - m_posle) / (m_do - m_st) * 100).toFixed(2);
            
            const resultField = document.getElementById('container_a_result');
            if (resultField) {
                resultField.value = result;
            }
            
            calculateWeightChange();
        }
    }
    
    // === РАСЧЕТ ИЗМЕНЕНИЯ МАССЫ ДЛЯ КОНТЕЙНЕРА B (ГОСТ 33140) ===
    function calculateContainerB() {
        const m_st = parseFloat(document.getElementById('container_b_weight')?.value) || 0;
        const m_do = parseFloat(document.getElementById('container_b_bitumen_before')?.value) || 0;
        const m_posle = parseFloat(document.getElementById('container_b_bitumen_after')?.value) || 0;
        
        if (m_st > 0 && m_do > m_st && m_posle > 0) {
            // Формула: Δm = (m_до - m_после) / (m_до - m_ст) × 100%
            const result = ((m_do - m_posle) / (m_do - m_st) * 100).toFixed(2);
            
            const resultField = document.getElementById('container_b_result');
            if (resultField) {
                resultField.value = result;
            }
            
            calculateWeightChange();
        }
    }
    
    // === РАСЧЕТ ОБЩЕГО ИЗМЕНЕНИЯ МАССЫ ===
    function calculateWeightChange() {
        const resultA = parseFloat(document.getElementById('container_a_result')?.value) || 0;
        const resultB = parseFloat(document.getElementById('container_b_result')?.value) || 0;
        const max = parseFloat(document.getElementById('weight_change_max')?.value) || 0.8;
        
        if (resultA > 0 && resultB > 0) {
            const average = ((resultA + resultB) / 2).toFixed(2);
            const field = document.getElementById('weight_change');
            
            if (field) {
                field.value = average;
                
                // Проверка превышения нормы
                if (parseFloat(average) > max) {
                    field.classList.add('input-alert');
                } else {
                    field.classList.remove('input-alert');
                }
            }
        }
    }
    
    // === ПРОВЕРКА ИЗМЕНЕНИЯ ТЕМПЕРАТУРЫ РАЗМЯГЧЕНИЯ ===
    function validateSofteningTemperatureChange() {
        const value = parseFloat(document.getElementById('softening_temperature_change')?.value) || 0;
        const max = parseFloat(document.getElementById('softening_temperature_change_max')?.value) || 7;
        const field = document.getElementById('softening_temperature_change');
        
        if (field && value > 0) {
            if (value > max) {
                field.classList.add('input-alert');
            } else {
                field.classList.remove('input-alert');
            }
        }
    }
    
    // === ПРИВЯЗКА ОБРАБОТЧИКОВ СОБЫТИЙ ===
    
    // Глубина проникания иглы
    const needleDeep = document.getElementById('needle_deep');
    if (needleDeep) {
        needleDeep.addEventListener('input', validateNeedleDeep);
        needleDeep.addEventListener('change', validateNeedleDeep);
    }
    
    // Температура размягчения
    const softeningTemp = document.getElementById('softening_temperature');
    if (softeningTemp) {
        softeningTemp.addEventListener('input', validateSofteningTemperature);
        softeningTemp.addEventListener('change', validateSofteningTemperature);
    }
    
    // Растяжимость
    const extensibility = document.getElementById('extensibility');
    if (extensibility) {
        extensibility.addEventListener('input', validateExtensibility);
        extensibility.addEventListener('change', validateExtensibility);
    }
    
    // Температура хрупкости
    const fragilityTemp = document.getElementById('fragility_temperature');
    if (fragilityTemp) {
        fragilityTemp.addEventListener('input', validateFragilityTemperature);
        fragilityTemp.addEventListener('change', validateFragilityTemperature);
    }
    
    // Температура вспышки
    const flashTemp = document.getElementById('flash_temperature');
    if (flashTemp) {
        flashTemp.addEventListener('input', validateFlashTemperature);
        flashTemp.addEventListener('change', validateFlashTemperature);
    }
    
    // Контейнер А
    ['container_a_weight', 'container_a_bitumen_before', 'container_a_bitumen_after'].forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', calculateContainerA);
            element.addEventListener('change', calculateContainerA);
        }
    });
    
    // Контейнер B
    ['container_b_weight', 'container_b_bitumen_before', 'container_b_bitumen_after'].forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', calculateContainerB);
            element.addEventListener('change', calculateContainerB);
        }
    });
    
    // Изменение температуры размягчения
    const softeningChange = document.getElementById('softening_temperature_change');
    if (softeningChange) {
        softeningChange.addEventListener('input', validateSofteningTemperatureChange);
        softeningChange.addEventListener('change', validateSofteningTemperatureChange);
    }
    
    // === ИНИЦИАЛИЗАЦИЯ ПРИ ЗАГРУЗКЕ ===
    validateNeedleDeep();
    validateSofteningTemperature();
    validateExtensibility();
    validateFragilityTemperature();
    validateFlashTemperature();
    calculateContainerA();
    calculateContainerB();
    validateSofteningTemperatureChange();
    
    // === ОБРАБОТКА ОТПРАВКИ ФОРМЫ ===
    const form = document.getElementById('bitumen-33133-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Здесь можно добавить дополнительную валидацию перед отправкой
            console.log('Форма битума ГОСТ 33133-2014 отправлена');
        });
    }
    
    // === БЛОКИРОВКА ENTER И СТРЕЛОК ===
    document.getElementById('bitumen-33133-form')?.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.keyCode === 40 || e.keyCode === 38) {
            e.preventDefault();
        }
    });
    
    console.log('Скрипт расчетов для битума ГОСТ 33133-2014 загружен');
});
