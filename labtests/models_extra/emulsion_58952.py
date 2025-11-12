"""Модель для хранения результатов испытаний битумной эмульсии по ГОСТ 58952.1-2020"""

from django.db import models


class EmulsionTestResult(models.Model):
    """Модель для хранения результатов испытаний битумной эмульсии по ГОСТ 58952.1-2020"""
    
    # Связь с образцом - используем строковую ссылку для избежания циклических импортов
    sample = models.OneToOneField(
        'labtests.TestSample',
        on_delete=models.CASCADE,
        related_name='emulsion_result'
    )
    
    # === ОБЛАСТЬ ПРИМЕНЕНИЯ ===
    apply_area = models.IntegerField(default=0, verbose_name="Область применения")  
    # 0-Общие, 1-Подгрунтовка, 2-Ямочный ремонт, 3-ШПО, 4-Рейсаклирование, 5-ЛЭМС
    
    # === ВНЕШНИЙ ВИД ===
    appearance = models.CharField(max_length=100, blank=True, null=True, verbose_name="Внешний вид")
    
    # === ИНДЕКС РАСПАДА ===
    decay_index_w1 = models.FloatField(blank=True, null=True, verbose_name="Масса чаши со шпателем, г")
    decay_index_w2 = models.FloatField(blank=True, null=True, verbose_name="Масса чаши со шпателем и с эмульсией, г")
    decay_index_w3 = models.FloatField(blank=True, null=True, verbose_name="Масса чаши со шпателем, эмульсией и кварцевым песком, г")
    decay_index_value = models.FloatField(blank=True, null=True, verbose_name="Индекс распада")
    decay_index_min = models.FloatField(blank=True, null=True, verbose_name="Индекс распада минимум")
    decay_index_max = models.FloatField(blank=True, null=True, verbose_name="Индекс распада максимум")
    
    # === УСЛОВНАЯ ВЯЗКОСТЬ ===
    viscosity_time = models.FloatField(blank=True, null=True, verbose_name="Время истечения, с")
    viscosity_value = models.FloatField(blank=True, null=True, verbose_name="Условная вязкость")
    viscosity_min = models.FloatField(default=10, verbose_name="Минимум")
    viscosity_max = models.FloatField(default=50, verbose_name="Максимум")
    
    # === pH ===
    ph_value = models.FloatField(blank=True, null=True, verbose_name="pH")
    ph_min = models.FloatField(default=2, verbose_name="Минимум pH")
    ph_max = models.FloatField(default=7, verbose_name="Максимум pH")
    
    # === МАССОВАЯ ДОЛЯ ОСТАТКА НА СИТЕ ===
    # Сито №0.8
    sieve_08_container_weight = models.FloatField(blank=True, null=True, verbose_name="Масса бюксы")
    sieve_08_container_with_residue = models.FloatField(blank=True, null=True, verbose_name="Масса бюксы с остатком")
    sieve_08_emulsion_weight = models.FloatField(blank=True, null=True, verbose_name="Масса эмульсии")
    sieve_08_residue_percent = models.FloatField(blank=True, null=True, verbose_name="Массовая доля остатка %")
    sieve_08_max = models.FloatField(default=0.08, verbose_name="Максимум")
    
    # Сито №0.14
    sieve_014_container_weight = models.FloatField(blank=True, null=True, verbose_name="Масса бюксы")
    sieve_014_container_with_residue = models.FloatField(blank=True, null=True, verbose_name="Масса бюксы с остатком")
    sieve_014_emulsion_weight = models.FloatField(blank=True, null=True, verbose_name="Масса эмульсии")
    sieve_014_residue_percent = models.FloatField(blank=True, null=True, verbose_name="Массовая доля остатка %")
    sieve_014_max = models.FloatField(default=0.2, verbose_name="Максимум")
    
    # === СОДЕРЖАНИЕ ВЯЖУЩЕГО С ЭМУЛЬГАТОРОМ ===
    binder_content_w1 = models.FloatField(blank=True, null=True, verbose_name="Масса чаши, г")
    binder_content_w2 = models.FloatField(blank=True, null=True, verbose_name="Масса эмульсии, г")
    binder_content_w3 = models.FloatField(blank=True, null=True, verbose_name="Масса чаши с эмульсией после выпаривания, г")
    binder_content_value = models.FloatField(blank=True, null=True, verbose_name="Содержание вяжущего с эмульгатором, %")
    binder_content_min = models.FloatField(default=50, verbose_name="Минимум")
    binder_content_max = models.FloatField(default=60, verbose_name="Максимум")
    
    # === МАССОВАЯ ДОЛЯ ВЯЖУЩЕГО С ЭМУЛЬГАТОРОМ (дополнительные пробы) ===
    binder_1_container_weight = models.FloatField(blank=True, null=True, verbose_name="Масса чашки 1")
    binder_1_emulsion_before = models.FloatField(blank=True, null=True, verbose_name="Масса эмульсии до выпаривания 1")
    binder_1_after_evaporation = models.FloatField(blank=True, null=True, verbose_name="Масса после выпаривания 1")
    binder_1_content = models.FloatField(blank=True, null=True, verbose_name="Массовая доля вяжущего 1, %")
    
    binder_2_container_weight = models.FloatField(blank=True, null=True, verbose_name="Масса чашки 2")
    binder_2_emulsion_before = models.FloatField(blank=True, null=True, verbose_name="Масса эмульсии до выпаривания 2")
    binder_2_after_evaporation = models.FloatField(blank=True, null=True, verbose_name="Масса после выпаривания 2")
    binder_2_content = models.FloatField(blank=True, null=True, verbose_name="Массовая доля вяжущего 2, %")
    
    binder_average = models.FloatField(blank=True, null=True, verbose_name="Средняя массовая доля вяжущего, %")
    binder_min = models.FloatField(default=50, verbose_name="Минимум")
    binder_max = models.FloatField(default=60, verbose_name="Максимум")
    
    # === ОСТАТОК НА СИТЕ 0.14 ===
    remaining_w1 = models.FloatField(blank=True, null=True, verbose_name="Масса сита 0.14, г")
    remaining_w2 = models.FloatField(blank=True, null=True, verbose_name="Масса стеклянного стакана, г")
    remaining_w3 = models.FloatField(blank=True, null=True, verbose_name="Масса эмульсии, г")
    remaining_w4 = models.FloatField(blank=True, null=True, verbose_name="Масса стакана с остатком эмульсии, г")
    remaining_w5 = models.FloatField(blank=True, null=True, verbose_name="Масса сита 0.14 с остатком после высушивания, г")
    remaining_value = models.FloatField(blank=True, null=True, verbose_name="Остаток на сите, %")
    remaining_max = models.FloatField(default=0.2, verbose_name="Максимум")
    
    # === ОСТАТОК НА СИТЕ 0.14 ПОСЛЕ 7 СУТОК ===
    remaining_after7_w1 = models.FloatField(blank=True, null=True, verbose_name="Масса сита 0.14, г")
    remaining_after7_w2 = models.FloatField(blank=True, null=True, verbose_name="Масса стеклянного стакана, г")
    remaining_after7_w3 = models.FloatField(blank=True, null=True, verbose_name="Масса эмульсии, г")
    remaining_after7_w4 = models.FloatField(blank=True, null=True, verbose_name="Масса стакана с остатком эмульсии, г")
    remaining_after7_w5 = models.FloatField(blank=True, null=True, verbose_name="Масса сита 0.14 с остатком после высушивания, г")
    remaining_after7_value = models.FloatField(blank=True, null=True, verbose_name="Остаток на сите после 7 суток, %")
    remaining_after7_max = models.FloatField(default=0.5, verbose_name="Максимум")
    
    # === УСТОЙЧИВОСТЬ К РАССЛОЕНИЮ ПРИ ХРАНЕНИИ 7 СУТОК ===
    resistance_cylinder1_volume = models.FloatField(blank=True, null=True, verbose_name="Объем эмульсии цилиндр 1")
    resistance_cylinder1_volume_after7 = models.FloatField(blank=True, null=True, verbose_name="Отметка после 7 суток цилиндр 1")
    resistance_cylinder1_delamination = models.FloatField(blank=True, null=True, verbose_name="Расслоение цилиндр 1, %")
    
    resistance_cylinder2_volume = models.FloatField(blank=True, null=True, verbose_name="Объем эмульсии цилиндр 2")
    resistance_cylinder2_volume_after7 = models.FloatField(blank=True, null=True, verbose_name="Отметка после 7 суток цилиндр 2")
    resistance_cylinder2_delamination = models.FloatField(blank=True, null=True, verbose_name="Расслоение цилиндр 2, %")
    
    resistance_after7_value = models.FloatField(blank=True, null=True, verbose_name="Устойчивость к расслоению, %")
    resistance_after7_max = models.FloatField(default=1.0, verbose_name="Максимум")
    
    # === АДГЕЗИЯ К МИНЕРАЛЬНОМУ МАТЕРИАЛУ ===
    mineral_material_adhesion = models.FloatField(blank=True, null=True, verbose_name="Масса эмульсии для минерального материала, г")
    visual_quality = models.IntegerField(default=1, verbose_name="Характеристика пленки")  # 1-Хорошо, 2-Удовлетворительно, 3-Неудовлетворительно
    
    # === УСТОЙЧИВОСТЬ ПРИ ХРАНЕНИИ ===
    # 7 суток
    stability_7_container_weight = models.FloatField(blank=True, null=True, verbose_name="Масса стакана")
    stability_7_sample_weight = models.FloatField(blank=True, null=True, verbose_name="Масса пробы эмульсии")
    stability_7_residue_weight = models.FloatField(blank=True, null=True, verbose_name="Масса остатка на сите")
    stability_7_percent = models.FloatField(blank=True, null=True, verbose_name="Устойчивость 7 суток, %")
    stability_7_max = models.FloatField(default=0.5, verbose_name="Максимум")
    
    # 30 суток
    stability_30_container_weight = models.FloatField(blank=True, null=True, verbose_name="Масса стакана")
    stability_30_sample_weight = models.FloatField(blank=True, null=True, verbose_name="Масса пробы эмульсии")
    stability_30_residue_weight = models.FloatField(blank=True, null=True, verbose_name="Масса остатка на сите")
    stability_30_percent = models.FloatField(blank=True, null=True, verbose_name="Устойчивость 30 суток, %")
    stability_30_max = models.FloatField(default=1, verbose_name="Максимум")
    
    # === УСТОЙЧИВОСТЬ К ПЕРЕМЕШИВАНИЮ ===
    mixing_container_weight = models.FloatField(blank=True, null=True, verbose_name="Масса стакана")
    mixing_sample_weight = models.FloatField(blank=True, null=True, verbose_name="Масса пробы эмульсии")
    mixing_residue_weight = models.FloatField(blank=True, null=True, verbose_name="Масса остатка на сите")
    mixing_stability_percent = models.FloatField(blank=True, null=True, verbose_name="Устойчивость к перемешиванию, %")
    mixing_stability_max = models.FloatField(default=0.5, verbose_name="Максимум")
    
    # === УСТОЙЧИВОСТЬ ПРИ ТРАНСПОРТИРОВАНИИ ===
    transport_stability = models.CharField(max_length=100, blank=True, null=True, verbose_name="Устойчивость при транспортировании")
    
    # === СЦЕПЛЕНИЕ С МИНЕРАЛЬНЫМИ МАТЕРИАЛАМИ ===
    adhesion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Сцепление")
    adhesion_norm = models.CharField(max_length=100, default="полное покрытие поверхности, не смывается", verbose_name="Норматив")
    
    # === ГЛУБИНА ПРОНИКАНИЯ ИГЛЫ В ОСТАТОК ===
    needle_penetration_1 = models.FloatField(blank=True, null=True, verbose_name="Глубина проникания 1, 0.1 мм")
    needle_penetration_2 = models.FloatField(blank=True, null=True, verbose_name="Глубина проникания 2, 0.1 мм")
    needle_penetration_3 = models.FloatField(blank=True, null=True, verbose_name="Глубина проникания 3, 0.1 мм")
    needle_penetration_average = models.FloatField(blank=True, null=True, verbose_name="Среднее значение, 0.1 мм")
    needle_penetration_min = models.FloatField(default=60, verbose_name="Минимум")
    needle_penetration_max = models.FloatField(default=130, verbose_name="Максимум")
    
    # === ТЕМПЕРАТУРА РАЗМЯГЧЕНИЯ ОСТАТКА ===
    softening_temp_1 = models.FloatField(blank=True, null=True, verbose_name="Температура размягчения 1, °C")
    softening_temp_2 = models.FloatField(blank=True, null=True, verbose_name="Температура размягчения 2, °C")
    softening_temp_average = models.FloatField(blank=True, null=True, verbose_name="Средняя температура, °C")
    softening_temp_min = models.FloatField(default=47, verbose_name="Минимум")
    
    # === ЭЛАСТИЧНОСТЬ ОСТАТКА ПРИ 25°С ===
    elasticity_1 = models.FloatField(blank=True, null=True, verbose_name="Эластичность 1, см")
    elasticity_2 = models.FloatField(blank=True, null=True, verbose_name="Эластичность 2, см")
    elasticity_3 = models.FloatField(blank=True, null=True, verbose_name="Эластичность 3, см")
    elasticity_average = models.FloatField(blank=True, null=True, verbose_name="Среднее значение, см")
    elasticity_min = models.FloatField(default=80, verbose_name="Минимум")
    
    # === ДОПОЛНИТЕЛЬНЫЕ ПОЛЯ ===
    test_date = models.DateField(blank=True, null=True, verbose_name="Дата испытания")
    tester_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="ФИО испытателя")
    notes = models.TextField(blank=True, null=True, verbose_name="Примечания")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Результат испытания эмульсии'
        verbose_name_plural = 'Результаты испытаний эмульсии'
    
    def __str__(self):
        return f"Эмульсия - {self.sample.sample_number}"
