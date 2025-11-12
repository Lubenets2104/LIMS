// Добавляем в конец файла sample_test_calculations.js

// Функция для расчета влажности (полная версия)
function calculateHumidityFull() {
    console.log('calculateHumidityFull called');
    
    // Первый образец
    const container1 = document.getElementById('humidity_1_container');
    const withSand1 = document.getElementById('humidity_1_with_sand');
    const afterDry1 = document.getElementById('humidity_1_after_dry');
    const value1 = document.getElementById('humidity_1_value');
    const hidden1 = document.getElementById('humidity_1_value_hidden');
    
    if (container1 && withSand1 && afterDry1 && value1) {
        const c1 = parseFloat(container1.value);
        const ws1 = parseFloat(withSand1.value);
        const ad1 = parseFloat(afterDry1.value);
        
        console.log('Образец 1:', { container: c1, withSand: ws1, afterDry: ad1 });
        
        if (!isNaN(c1) && !isNaN(ws1) && !isNaN(ad1)) {
            if (ws1 <= c1) {
                console.log('Ошибка: Масса с песком должна быть больше массы контейнера');
                value1.value = '';
            } else if (ad1 <= c1) {
                console.log('Ошибка: Масса после сушки должна быть больше массы контейнера');
                value1.value = '';
            } else if (ad1 >= ws1) {
                console.log('Ошибка: Масса после сушки должна быть меньше массы с песком');
                value1.value = '';
            } else {
                const humidity1 = ((ws1 - ad1) / (ad1 - c1)) * 100;
                const rounded1 = Math.round(humidity1 * 100) / 100;
                value1.value = rounded1;
                if (hidden1) hidden1.value = rounded1;
                console.log(`Влажность 1 рассчитана: ${rounded1}%`);
            }
        }
    }
    
    // Второй образец
    const container2 = document.getElementById('humidity_2_container');
    const withSand2 = document.getElementById('humidity_2_with_sand');
    const afterDry2 = document.getElementById('humidity_2_after_dry');
    const value2 = document.getElementById('humidity_2_value');
    const hidden2 = document.getElementById('humidity_2_value_hidden');
    
    if (container2 && withSand2 && afterDry2 && value2) {
        const c2 = parseFloat(container2.value);
        const ws2 = parseFloat(withSand2.value);
        const ad2 = parseFloat(afterDry2.value);
        
        console.log('Образец 2:', { container: c2, withSand: ws2, afterDry: ad2 });
        
        if (!isNaN(c2) && !isNaN(ws2) && !isNaN(ad2)) {
            if (ws2 <= c2) {
                console.log('Ошибка: Масса с песком должна быть больше массы контейнера');
                value2.value = '';
            } else if (ad2 <= c2) {
                console.log('Ошибка: Масса после сушки должна быть больше массы контейнера');
                value2.value = '';
            } else if (ad2 >= ws2) {
                console.log('Ошибка: Масса после сушки должна быть меньше массы с песком');
                value2.value = '';
            } else {
                const humidity2 = ((ws2 - ad2) / (ad2 - c2)) * 100;
                const rounded2 = Math.round(humidity2 * 100) / 100;
                value2.value = rounded2;
                if (hidden2) hidden2.value = rounded2;
                console.log(`Влажность 2 рассчитана: ${rounded2}%`);
            }
        }
    }
    
    // Среднее значение
    const average = document.getElementById('humidity_average');
    const hiddenAvg = document.getElementById('humidity_average_hidden');
    
    if (average && value1 && value2) {
        const v1 = parseFloat(value1.value);
        const v2 = parseFloat(value2.value);
        
        if (!isNaN(v1) && !isNaN(v2)) {
            const avg = (v1 + v2) / 2;
            const roundedAvg = Math.round(avg * 100) / 100;
            average.value = roundedAvg;
            if (hiddenAvg) hiddenAvg.value = roundedAvg;
        } else if (!isNaN(v1)) {
            average.value = v1;
            if (hiddenAvg) hiddenAvg.value = v1;
        } else if (!isNaN(v2)) {
            average.value = v2;
            if (hiddenAvg) hiddenAvg.value = v2;
        }
    }
}

// Добавляем обработчики событий для полей влажности
document.addEventListener('DOMContentLoaded', function() {
    // Обработчики для влажности
    const humidityFields = [
        'humidity_1_container', 'humidity_1_with_sand', 'humidity_1_after_dry',
        'humidity_2_container', 'humidity_2_with_sand', 'humidity_2_after_dry'
    ];
    
    humidityFields.forEach(id => {
        const field = document.getElementById(id);
        if (field) {
            field.addEventListener('input', calculateHumidityFull);
            field.addEventListener('change', calculateHumidityFull);
        }
    });
    
    // Запускаем расчет при загрузке
    setTimeout(calculateHumidityFull, 500);
});
