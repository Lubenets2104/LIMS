# Модель для ГОСТ 8267-93 (Щебень и гравий из плотных горных пород для строительных работ)

from django.db import models

class Crushed8267TestResult(models.Model):
    """Модель для хранения результатов испытаний щебня по ГОСТ 8267-93"""
    
    sample = models.OneToOneField(
        'TestSample',
        on_delete=models.CASCADE,
        related_name='crushed_8267_result'
    )
    
    # === ГРАНУЛОМЕТРИЧЕСКИЙ СОСТАВ ===
    grain_compound_weight = models.FloatField(blank=True, null=True, verbose_name="Масса пробы, г")
    
    # Размеры отверстий контрольных сит (стандартные фракции)
    # Для фракции 5-10, 5-20, 10-20, 20-40, 40-70 и т.д.
    
    # 70 мм
    sieve_70_weight = models.FloatField(blank=True, null=True)
    sieve_70_partial = models.FloatField(blank=True, null=True)
    sieve_70_full = models.FloatField(blank=True, null=True)
    
    # 40 мм
    sieve_40_weight = models.FloatField(blank=True, null=True)
    sieve_40_partial = models.FloatField(blank=True, null=True)
    sieve_40_full = models.FloatField(blank=True, null=True)
    
    # 20 мм
    sieve_20_weight = models.FloatField(blank=True, null=True)
    sieve_20_partial = models.FloatField(blank=True, null=True)
    sieve_20_full = models.FloatField(blank=True, null=True)
    
    # 10 мм
    sieve_10_weight = models.FloatField(blank=True, null=True)
    sieve_10_partial = models.FloatField(blank=True, null=True)
    sieve_10_full = models.FloatField(blank=True, null=True)
    
    # 5 мм
    sieve_5_weight = models.FloatField(blank=True, null=True)
    sieve_5_partial = models.FloatField(blank=True, null=True)
    sieve_5_full = models.FloatField(blank=True, null=True)
    
    # 2.5 мм (для мелких фракций)
    sieve_2_5_weight = models.FloatField(blank=True, null=True)
    sieve_2_5_partial = models.FloatField(blank=True, null=True)
    sieve_2_5_full = models.FloatField(blank=True, null=True)
    
    # 1.25 мм (для мелких фракций)
    sieve_1_25_weight = models.FloatField(blank=True, null=True)
    sieve_1_25_partial = models.FloatField(blank=True, null=True)
    sieve_1_25_full = models.FloatField(blank=True, null=True)
    
    # Фракция (например, 5-10, 10-20, 20-40 и т.д.)
    fraction_type = models.CharField(max_length=50, blank=True, null=True)
    
    # === СОДЕРЖАНИЕ ПЫЛЕВИДНЫХ И ГЛИНИСТЫХ ЧАСТИЦ ===
    dust_initial_weight = models.FloatField(blank=True, null=True, verbose_name="Масса начальная, г")
    dust_after_weight = models.FloatField(blank=True, null=True, verbose_name="Масса после отмучивания, г")
    dust_content = models.FloatField(blank=True, null=True, verbose_name="Содержание п/г частиц, %")
    
    # === СОДЕРЖАНИЕ ГЛИНЫ В КОМКАХ ===
    clay_initial_weight = models.FloatField(blank=True, null=True, verbose_name="Масса пробы, г")
    clay_weight = models.FloatField(blank=True, null=True, verbose_name="Масса глины в комках, г")
    clay_content = models.FloatField(blank=True, null=True, verbose_name="Содержание глины в комках, %")
    
    # === ЛЕЩАДНОСТЬ (содержание зерен пластинчатой и игловатой формы) ===
    # Для разных фракций
    flakiness_5_10_weight = models.FloatField(blank=True, null=True)
    flakiness_5_10_flaky_weight = models.FloatField(blank=True, null=True)
    flakiness_5_10_value = models.FloatField(blank=True, null=True)
    
    flakiness_10_20_weight = models.FloatField(blank=True, null=True)
    flakiness_10_20_flaky_weight = models.FloatField(blank=True, null=True)
    flakiness_10_20_value = models.FloatField(blank=True, null=True)
    
    flakiness_20_40_weight = models.FloatField(blank=True, null=True)
    flakiness_20_40_flaky_weight = models.FloatField(blank=True, null=True)
    flakiness_20_40_value = models.FloatField(blank=True, null=True)
    
    flakiness_40_70_weight = models.FloatField(blank=True, null=True)
    flakiness_40_70_flaky_weight = models.FloatField(blank=True, null=True)
    flakiness_40_70_value = models.FloatField(blank=True, null=True)
    
    flakiness_average = models.FloatField(blank=True, null=True, verbose_name="Средняя лещадность, %")
    flakiness_group = models.CharField(max_length=10, blank=True, null=True, verbose_name="Группа по лещадности")
    
    # === ДРОБИМОСТЬ ===
    crushability_type = models.IntegerField(default=0, verbose_name="Тип породы")  # 0 - изверженные, 1 - осадочные
    
    # Для разных фракций
    crushability_5_10_weight = models.FloatField(blank=True, null=True)
    crushability_5_10_after_weight = models.FloatField(blank=True, null=True)
    crushability_5_10_value = models.FloatField(blank=True, null=True)
    
    crushability_10_20_weight = models.FloatField(blank=True, null=True)
    crushability_10_20_after_weight = models.FloatField(blank=True, null=True)
    crushability_10_20_value = models.FloatField(blank=True, null=True)
    
    crushability_20_40_weight = models.FloatField(blank=True, null=True)
    crushability_20_40_after_weight = models.FloatField(blank=True, null=True)
    crushability_20_40_value = models.FloatField(blank=True, null=True)
    
    crushability_average = models.FloatField(blank=True, null=True, verbose_name="Средняя дробимость, %")
    crushability_mark = models.CharField(max_length=50, blank=True, null=True, verbose_name="Марка по дробимости")
    
    # === ИСТИРАЕМОСТЬ ===
    abrasion_weight = models.FloatField(blank=True, null=True, verbose_name="Масса пробы, г")
    abrasion_after_weight = models.FloatField(blank=True, null=True, verbose_name="Масса после испытания, г")
    abrasion_value = models.FloatField(blank=True, null=True, verbose_name="Истираемость, %")
    abrasion_mark = models.CharField(max_length=10, blank=True, null=True, verbose_name="Марка по истираемости")
    
    # === МОРОЗОСТОЙКОСТЬ ===
    frost_resistance_mark = models.CharField(max_length=10, blank=True, null=True, verbose_name="Марка по морозостойкости")
    frost_cycles = models.IntegerField(blank=True, null=True, verbose_name="Количество циклов")
    frost_weight_loss = models.FloatField(blank=True, null=True, verbose_name="Потеря массы, %")
    
    # === НАСЫПНАЯ ПЛОТНОСТЬ ===
    bulk_density_1_volume = models.FloatField(blank=True, null=True)
    bulk_density_1_empty = models.FloatField(blank=True, null=True)
    bulk_density_1_full = models.FloatField(blank=True, null=True)
    bulk_density_1_density = models.FloatField(blank=True, null=True)
    
    bulk_density_2_volume = models.FloatField(blank=True, null=True)
    bulk_density_2_empty = models.FloatField(blank=True, null=True)
    bulk_density_2_full = models.FloatField(blank=True, null=True)
    bulk_density_2_density = models.FloatField(blank=True, null=True)
    
    bulk_density_average = models.FloatField(blank=True, null=True, verbose_name="Средняя насыпная плотность, кг/м³")
    
    # === ИСТИННАЯ ПЛОТНОСТЬ ===
    true_density_1_number = models.CharField(max_length=50, blank=True)
    true_density_1_weight = models.FloatField(blank=True, null=True)
    true_density_1_volume = models.FloatField(blank=True, null=True)
    true_density_1_density = models.FloatField(blank=True, null=True)
    
    true_density_2_number = models.CharField(max_length=50, blank=True)
    true_density_2_weight = models.FloatField(blank=True, null=True)
    true_density_2_volume = models.FloatField(blank=True, null=True)
    true_density_2_density = models.FloatField(blank=True, null=True)
    
    true_density_average = models.FloatField(blank=True, null=True, verbose_name="Средняя истинная плотность, г/см³")
    
    # === ПУСТОТНОСТЬ ===
    void_content = models.FloatField(blank=True, null=True, verbose_name="Пустотность, %")
    
    # === ВОДОПОГЛОЩЕНИЕ ===
    water_absorption = models.FloatField(blank=True, null=True, verbose_name="Водопоглощение, %")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Результат испытания щебня по ГОСТ 8267-93'
        verbose_name_plural = 'Результаты испытаний щебня по ГОСТ 8267-93'
    
    def __str__(self):
        return f"Щебень 8267 - {self.sample.sample_number}"
