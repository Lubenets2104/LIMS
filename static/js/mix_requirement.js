// Обновляем обязательность поля смеси при изменении ГОСТа
function updateMixRequirement() {
    const gostSelect = document.getElementById('id_gost');
    const mixSelect = document.getElementById('id_mix');
    const mixLabel = document.querySelector('label[for="id_mix"]');
    
    if (gostSelect && mixSelect && gostSelect.value) {
        // Проверяем, есть ли опции в select для смеси (кроме пустой)
        if (mixSelect.options.length > 1) {
            // Есть смеси - делаем поле обязательным
            mixSelect.required = true;
            if (mixLabel && !mixLabel.innerHTML.includes('*')) {
                mixLabel.innerHTML = 'Смесь <span style="color: red;">*</span>';
            }
        } else {
            // Нет смесей - поле необязательное
            mixSelect.required = false;
            if (mixLabel) {
                mixLabel.innerHTML = 'Смесь';
            }
        }
    }
}

// Вызываем при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    const gostSelect = document.getElementById('id_gost');
    
    if (gostSelect) {
        // При изменении ГОСТа
        gostSelect.addEventListener('change', function() {
            setTimeout(updateMixRequirement, 500); // Задержка для загрузки смесей
        });
        
        // При загрузке страницы
        setTimeout(updateMixRequirement, 500);
    }
    
    // Также обновляем при изменении списка смесей
    const mixSelect = document.getElementById('id_mix');
    if (mixSelect) {
        const observer = new MutationObserver(function(mutations) {
            updateMixRequirement();
        });
        
        observer.observe(mixSelect, { childList: true });
    }
});
