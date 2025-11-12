"""
Модель для минерального порошка по ГОСТ 32761-2014
"""
from django.db import models
from labtests.models import TestSample


class MineralPowderTestResult(models.Model):
    """Результаты испытаний минерального порошка по ГОСТ 32761-2014"""
    
    sample = models.OneToOneField(TestSample, on_delete=models.CASCADE, related_name='mineral_powder_result')
    
    # === ГРАНУЛОМЕТРИЧЕСКИЙ СОСТАВ ===
    # Масса пробы
    sample_weight = models.FloatField('Масса пробы, г', null=True, blank=True)
    
    # Навески для сит (размеры: 2-0.125, 0.125, 0.063, <0.063)
    sieve_2_0125_weight = models.FloatField('Навеска 2-0.125 мм', null=True, blank=True)
    sieve_0125_weight = models.FloatField('Навеска 0.125 мм', null=True, blank=True)
    sieve_0063_weight = models.FloatField('Навеска 0.063 мм', null=True, blank=True)
    sieve_less_0063_weight = models.FloatField('Навеска <0.063 мм', null=True, blank=True)
    
    # Частный остаток (рассчитывается)
    sieve_2_0125_remainder = models.FloatField('Частный остаток 2-0.125 мм', null=True, blank=True)
    sieve_0125_remainder = models.FloatField('Частный остаток 0.125 мм', null=True, blank=True)
    sieve_0063_remainder = models.FloatField('Частный остаток 0.063 мм', null=True, blank=True)
    sieve_less_0063_remainder = models.FloatField('Частный остаток <0.063 мм', null=True, blank=True)
    
    # Полный остаток (рассчитывается)
    sieve_2_0125_full_remainder = models.FloatField('Полный остаток 2-0.125 мм', null=True, blank=True)
    sieve_0125_full_remainder = models.FloatField('Полный остаток 0.125 мм', null=True, blank=True)
    sieve_0063_full_remainder = models.FloatField('Полный остаток 0.063 мм', null=True, blank=True)
    sieve_less_0063_full_remainder = models.FloatField('Полный остаток <0.063 мм', null=True, blank=True)
    
    # Полный проход (рассчитывается)
    sieve_2_0125_passes = models.FloatField('Полный проход 2-0.125 мм', null=True, blank=True)
    sieve_0125_passes = models.FloatField('Полный проход 0.125 мм', null=True, blank=True)
    sieve_0063_passes = models.FloatField('Полный проход 0.063 мм', null=True, blank=True)
    sieve_less_0063_passes = models.FloatField('Полный проход <0.063 мм', null=True, blank=True)
    
    # === ВЛАЖНОСТЬ ===
    humidity_plate_weight_before = models.FloatField('Масса чаши и пробы до высушивания, г', null=True, blank=True)
    humidity_plate_weight_after = models.FloatField('Масса чаши и пробы после высушивания, г', null=True, blank=True)
    humidity_plate_weight = models.FloatField('Масса чаши, г', null=True, blank=True)
    humidity_value = models.FloatField('Влажность, %', null=True, blank=True)
    
    # === ИСТИННАЯ ПЛОТНОСТЬ (2 измерения) ===
    # Измерение 1
    real_density_1_weight_with_powder = models.FloatField('Масса колбы и мин.порошка 1, г', null=True, blank=True)
    real_density_1_empty_weight = models.FloatField('Масса пустой колбы 1, г', null=True, blank=True)
    real_density_1_weight_with_water = models.FloatField('Масса колбы с дистиллированной водой 1, г', null=True, blank=True)
    real_density_1_weight_with_powder_and_water = models.FloatField('Масса колбы с порошком и водой 1, г', null=True, blank=True)
    real_density_1_value = models.FloatField('Плотность 1, г/см3', null=True, blank=True)
    
    # Измерение 2
    real_density_2_weight_with_powder = models.FloatField('Масса колбы и мин.порошка 2, г', null=True, blank=True)
    real_density_2_empty_weight = models.FloatField('Масса пустой колбы 2, г', null=True, blank=True)
    real_density_2_weight_with_water = models.FloatField('Масса колбы с дистиллированной водой 2, г', null=True, blank=True)
    real_density_2_weight_with_powder_and_water = models.FloatField('Масса колбы с порошком и водой 2, г', null=True, blank=True)
    real_density_2_value = models.FloatField('Плотность 2, г/см3', null=True, blank=True)
    
    # Средняя истинная плотность
    real_density_average = models.FloatField('Средняя истинная плотность, г/см3', null=True, blank=True)
    
    # === СРЕДНЯЯ ПЛОТНОСТЬ ===
    average_density_bottom_weight_with_powder = models.FloatField('Масса нижней части цилиндра с порошком, г', null=True, blank=True)
    average_density_bottom_weight = models.FloatField('Масса нижней части цилиндра, г', null=True, blank=True)
    average_density_volume = models.FloatField('Объем МП', null=True, blank=True)
    average_density_value = models.FloatField('Средняя плотность', null=True, blank=True)
    porosity = models.FloatField('Пористость, %', null=True, blank=True)
    
    # === БИТУМОЕМКОСТЬ ===
    bitumen_capacity_weight = models.FloatField('Масса пробы мин.порошка, г', null=True, blank=True)
    bitumen_capacity_weight_after = models.FloatField('Масса оставшегося после испытания порошка, г', null=True, blank=True)
    bitumen_capacity_oil_weight = models.FloatField('Масса масла, г', null=True, blank=True)
    bitumen_capacity_real_density = models.FloatField('Истинная плотность для битумоемкости', null=True, blank=True)
    bitumen_capacity_value = models.FloatField('Битумоемкость', null=True, blank=True)
    
    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Результат испытания минерального порошка'
        verbose_name_plural = 'Результаты испытаний минерального порошка'
    
    def __str__(self):
        return f"Минеральный порошок - {self.sample.sample_number}"
