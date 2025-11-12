from django.db import models


class BitumenTestResult33133(models.Model):
    """
    Результаты испытаний битума по ГОСТ 33133-2014
    Битум нефтяной дорожный вязкий
    """
    
    # Связь с образцом - используем строковую ссылку для избежания циклических импортов
    sample = models.OneToOneField(
        'labtests.TestSample',
        on_delete=models.CASCADE,
        related_name='bitumen_33133_result'
    )
    
    # Глубина проникания иглы при 25°С
    needle_deep = models.FloatField(
        verbose_name='Глубина проникания иглы при 25°С, мм',
        null=True, blank=True
    )
    needle_deep_min = models.FloatField(
        verbose_name='Минимальная глубина проникания (норма)',
        null=True, blank=True
    )
    needle_deep_max = models.FloatField(
        verbose_name='Максимальная глубина проникания (норма)',
        null=True, blank=True
    )
    
    # Температура размягчения по кольцу и шару
    softening_temperature = models.FloatField(
        verbose_name='Температура размягчения, °С',
        null=True, blank=True
    )
    softening_temperature_min = models.FloatField(
        verbose_name='Минимальная температура размягчения (норма)',
        null=True, blank=True
    )
    
    # Растяжимость при 0°С
    extensibility = models.FloatField(
        verbose_name='Растяжимость при 0°С, см',
        null=True, blank=True
    )
    extensibility_min = models.FloatField(
        verbose_name='Минимальная растяжимость (норма)',
        null=True, blank=True
    )
    
    # Температура хрупкости
    fragility_temperature = models.FloatField(
        verbose_name='Температура хрупкости, °С',
        null=True, blank=True
    )
    fragility_temperature_max = models.FloatField(
        verbose_name='Максимальная температура хрупкости (норма)',
        null=True, blank=True
    )
    
    # Температура вспышки
    flash_temperature = models.FloatField(
        verbose_name='Температура вспышки, °С',
        null=True, blank=True
    )
    flash_temperature_min = models.FloatField(
        verbose_name='Минимальная температура вспышки (норма)',
        null=True, blank=True
    )
    
    # Изменение массы после старения - Контейнер А
    container_a_weight = models.FloatField(
        verbose_name='Масса стеклянного контейнера А, г',
        null=True, blank=True
    )
    container_a_bitumen_before = models.FloatField(
        verbose_name='Масса контейнера А с битумом до старения, г',
        null=True, blank=True
    )
    container_a_bitumen_after = models.FloatField(
        verbose_name='Масса контейнера А с битумом после старения, г',
        null=True, blank=True
    )
    container_a_result = models.FloatField(
        verbose_name='Результат контейнера А, %',
        null=True, blank=True,
        editable=False
    )
    
    # Изменение массы после старения - Контейнер B
    container_b_weight = models.FloatField(
        verbose_name='Масса стеклянного контейнера B, г',
        null=True, blank=True
    )
    container_b_bitumen_before = models.FloatField(
        verbose_name='Масса контейнера B с битумом до старения, г',
        null=True, blank=True
    )
    container_b_bitumen_after = models.FloatField(
        verbose_name='Масса контейнера B с битумом после старения, г',
        null=True, blank=True
    )
    container_b_result = models.FloatField(
        verbose_name='Результат контейнера B, %',
        null=True, blank=True,
        editable=False
    )
    
    # Общий итог изменения массы
    weight_change = models.FloatField(
        verbose_name='Изменение массы после старения, %',
        null=True, blank=True,
        editable=False
    )
    weight_change_max = models.FloatField(
        verbose_name='Максимальное изменение массы (норма)',
        null=True, blank=True
    )
    
    # Изменение температуры размягчения после старения
    softening_temperature_change = models.FloatField(
        verbose_name='Изменение температуры размягчения после старения, °С',
        null=True, blank=True
    )
    softening_temperature_change_max = models.FloatField(
        verbose_name='Максимальное изменение температуры (норма)',
        null=True, blank=True
    )
    
    def get_normatives(self):
        """Определяет нормативные значения в зависимости от марки битума"""
        # Нормативы по ГОСТ 33133-2014 (Таблица 1)
        normatives = {
            'БНД 130/200': {
                'needle_deep_min': 131, 'needle_deep_max': 200,
                'softening_temperature_min': 42,
                'extensibility_min': 6.0,
                'fragility_temperature_max': -21,
                'flash_temperature_min': 220,
                'weight_change_max': 0.8,
                'softening_temperature_change_max': 7
            },
            'БНД 100/130': {
                'needle_deep_min': 101, 'needle_deep_max': 130,
                'softening_temperature_min': 45,
                'extensibility_min': 4.0,
                'fragility_temperature_max': -20,
                'flash_temperature_min': 230,
                'weight_change_max': 0.7,
                'softening_temperature_change_max': 7
            },
            'БНД 70/100': {
                'needle_deep_min': 71, 'needle_deep_max': 100,
                'softening_temperature_min': 47,
                'extensibility_min': 3.7,
                'fragility_temperature_max': -18,
                'flash_temperature_min': 230,
                'weight_change_max': 0.6,
                'softening_temperature_change_max': 7
            },
            'БНД 50/70': {
                'needle_deep_min': 51, 'needle_deep_max': 70,
                'softening_temperature_min': 51,
                'extensibility_min': 3.5,
                'fragility_temperature_max': -16,
                'flash_temperature_min': 230,
                'weight_change_max': 0.6,
                'softening_temperature_change_max': 7
            },
            'БНД 35/50': {
                'needle_deep_min': 36, 'needle_deep_max': 50,
                'softening_temperature_min': 53,
                'extensibility_min': None,  # Не определяется по ГОСТ
                'fragility_temperature_max': -14,
                'flash_temperature_min': 230,
                'weight_change_max': 0.5,
                'softening_temperature_change_max': 6
            },
            'БНД 20/35': {
                'needle_deep_min': 20, 'needle_deep_max': 35,
                'softening_temperature_min': 55,
                'extensibility_min': None,  # Не определяется по ГОСТ
                'fragility_temperature_max': -11,
                'flash_temperature_min': 230,
                'weight_change_max': 0.5,
                'softening_temperature_change_max': 6
            },
        }
        
        # Определяем марку битума
        mix_name = self.sample.mix.name if self.sample.mix else 'БНД 100/130'
        
        # Ищем марку в словаре нормативов
        for key in normatives.keys():
            if key in mix_name:
                return normatives[key]
        
        # Если марка не найдена, возвращаем нормативы для БНД 100/130
        return normatives['БНД 100/130']
    
    def set_normatives(self):
        """Устанавливает нормативные значения в зависимости от марки"""
        norms = self.get_normatives()
        for field, value in norms.items():
            # Устанавливаем значение только если оно не None
            if value is not None:
                setattr(self, field, value)
    
    class Meta:
        verbose_name = 'Результат испытания битума ГОСТ 33133-2014'
        verbose_name_plural = 'Результаты испытаний битума ГОСТ 33133-2014'
        
    def save(self, *args, **kwargs):
        """Расчет автоматических полей"""
        
        # Расчет для контейнера А
        if all([self.container_a_weight, self.container_a_bitumen_before, 
                self.container_a_bitumen_after]):
            mass_before = self.container_a_bitumen_before - self.container_a_weight
            mass_after = self.container_a_bitumen_after - self.container_a_weight
            if mass_before > 0:
                self.container_a_result = round(
                    (mass_before - mass_after) / mass_before * 100, 2
                )
        
        # Расчет для контейнера B
        if all([self.container_b_weight, self.container_b_bitumen_before, 
                self.container_b_bitumen_after]):
            mass_before = self.container_b_bitumen_before - self.container_b_weight
            mass_after = self.container_b_bitumen_after - self.container_b_weight
            if mass_before > 0:
                self.container_b_result = round(
                    (mass_before - mass_after) / mass_before * 100, 2
                )
        
        # Среднее изменение массы
        if self.container_a_result is not None and self.container_b_result is not None:
            self.weight_change = round(
                (self.container_a_result + self.container_b_result) / 2, 2
            )
        
        super().save(*args, **kwargs)
    
    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if hasattr(self.sample, 'mix') and self.sample.mix:
            return f"Битум {self.sample.mix.name} - {self.sample.sample_number}"
        return f"Битум - {self.sample.sample_number}"
