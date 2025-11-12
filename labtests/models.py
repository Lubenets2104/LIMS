from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """Профиль пользователя с персональными настройками"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    department = models.CharField(max_length=100, blank=True, verbose_name='Отдел')
    position = models.CharField(max_length=100, blank=True, verbose_name='Должность')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f"{self.user.username} - {self.position or 'Сотрудник'}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создаем профиль при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняем профиль при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Material(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class GOST(models.Model):
    number = models.CharField(max_length=50)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='gosts')

    def __str__(self):
        return f"{self.number} ({self.material.name})"


class MixName(models.Model):
    name = models.CharField(max_length=100)
    gost = models.ForeignKey(GOST, on_delete=models.CASCADE, related_name='mixes')

    def __str__(self):
        return self.name


class Indicator(models.Model):
    name = models.CharField(max_length=100)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='indicators', null=True, blank=True)
    gost = models.ForeignKey(GOST, on_delete=models.CASCADE, related_name='indicators')

    def __str__(self):
        return self.name


class TestSample(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершено'),
    ]

    sample_number = models.CharField(max_length=50)
    sampling_date = models.DateField()
    received_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)

    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    gost = models.ForeignKey(GOST, on_delete=models.PROTECT)
    mix = models.ForeignKey(MixName, on_delete=models.PROTECT, null=True, blank=True)
    indicators = models.ManyToManyField(Indicator)

    customer = models.CharField(max_length=100)
    supplier = models.CharField(max_length=100)
    object_name = models.CharField(max_length=200)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Связь с пользователем
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_samples', null=True, blank=True)

    def __str__(self):
        return self.sample_number


class TestResult(models.Model):
    """Модель для хранения результатов испытаний песка"""
    sample = models.OneToOneField(TestSample, on_delete=models.CASCADE, related_name='test_result')
    result_class = models.CharField(max_length=20, default='I класс')
    
    # Зерновой состав и модуль крупности
    grain_initial_weight = models.FloatField(null=True, blank=True)
    grain_8_weight = models.FloatField(null=True, blank=True)
    grain_4_weight = models.FloatField(null=True, blank=True)
    grain_8_percent = models.FloatField(null=True, blank=True)
    grain_4_percent = models.FloatField(null=True, blank=True)
    
    # Пылевидные и глинистые частицы
    dust_initial_weight = models.FloatField(null=True, blank=True)
    dust_after_weight = models.FloatField(null=True, blank=True)
    dust_percent = models.FloatField(null=True, blank=True)
    
    # Зерновой состав (сита)
    sieve_2_weight = models.FloatField(null=True, blank=True)
    sieve_1_weight = models.FloatField(null=True, blank=True)
    sieve_05_weight = models.FloatField(null=True, blank=True)
    sieve_025_weight = models.FloatField(null=True, blank=True)
    sieve_0125_weight = models.FloatField(null=True, blank=True)
    
    sieve_2_partial = models.FloatField(null=True, blank=True)
    sieve_1_partial = models.FloatField(null=True, blank=True)
    sieve_05_partial = models.FloatField(null=True, blank=True)
    sieve_025_partial = models.FloatField(null=True, blank=True)
    sieve_0125_partial = models.FloatField(null=True, blank=True)
    
    sieve_2_full = models.FloatField(null=True, blank=True)
    sieve_1_full = models.FloatField(null=True, blank=True)
    sieve_05_full = models.FloatField(null=True, blank=True)
    sieve_025_full = models.FloatField(null=True, blank=True)
    sieve_0125_full = models.FloatField(null=True, blank=True)
    
    # Модуль крупности
    size_module_value = models.FloatField(null=True, blank=True)
    size_module_name = models.CharField(max_length=50, blank=True)
    
    # Глина в комках
    clay_initial_weight = models.FloatField(null=True, blank=True)
    clay_weight = models.FloatField(null=True, blank=True)
    clay_percent = models.FloatField(null=True, blank=True)
    
    # Влажность
    humidity_1_number = models.CharField(max_length=50, blank=True)
    humidity_1_container = models.FloatField(null=True, blank=True)
    humidity_1_with_sand = models.FloatField(null=True, blank=True)
    humidity_1_after_dry = models.FloatField(null=True, blank=True)
    humidity_1_value = models.FloatField(null=True, blank=True)
    
    humidity_2_number = models.CharField(max_length=50, blank=True)
    humidity_2_container = models.FloatField(null=True, blank=True)
    humidity_2_with_sand = models.FloatField(null=True, blank=True)
    humidity_2_after_dry = models.FloatField(null=True, blank=True)
    humidity_2_value = models.FloatField(null=True, blank=True)
    
    humidity_average = models.FloatField(null=True, blank=True)
    
    # Набухание глинистых частиц
    clay_swell_1_number = models.CharField(max_length=50, blank=True)
    clay_swell_1_initial = models.FloatField(null=True, blank=True)
    clay_swell_1_after = models.FloatField(null=True, blank=True)
    clay_swell_1_k = models.FloatField(null=True, blank=True)
    
    clay_swell_2_number = models.CharField(max_length=50, blank=True)
    clay_swell_2_initial = models.FloatField(null=True, blank=True)
    clay_swell_2_after = models.FloatField(null=True, blank=True)
    clay_swell_2_k = models.FloatField(null=True, blank=True)
    
    clay_swell_average_k = models.FloatField(null=True, blank=True)
    clay_swell_content = models.FloatField(null=True, blank=True)
    clay_swell_conclusion = models.CharField(max_length=100, blank=True)
    
    # Насыпная плотность
    bulk_1_volume = models.FloatField(null=True, blank=True)
    bulk_1_empty = models.FloatField(null=True, blank=True)
    bulk_1_full = models.FloatField(null=True, blank=True)
    bulk_1_density = models.FloatField(null=True, blank=True)
    
    bulk_2_volume = models.FloatField(null=True, blank=True)
    bulk_2_empty = models.FloatField(null=True, blank=True)
    bulk_2_full = models.FloatField(null=True, blank=True)
    bulk_2_density = models.FloatField(null=True, blank=True)
    
    bulk_average_density = models.FloatField(null=True, blank=True)
    
    # Истинная плотность
    actual_1_number = models.CharField(max_length=50, blank=True)
    actual_1_empty = models.FloatField(null=True, blank=True)
    actual_1_water = models.FloatField(null=True, blank=True)
    actual_1_sand = models.FloatField(null=True, blank=True)
    actual_1_full = models.FloatField(null=True, blank=True)
    actual_1_density = models.FloatField(null=True, blank=True)
    
    actual_2_number = models.CharField(max_length=50, blank=True)
    actual_2_empty = models.FloatField(null=True, blank=True)
    actual_2_water = models.FloatField(null=True, blank=True)
    actual_2_sand = models.FloatField(null=True, blank=True)
    actual_2_full = models.FloatField(null=True, blank=True)
    actual_2_density = models.FloatField(null=True, blank=True)
    
    actual_average_density = models.FloatField(null=True, blank=True)
    
    # Пустотность
    emptiness = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Результаты {self.sample.sample_number}"


class AsphaltTestResult(models.Model):
    """Модель для хранения результатов испытаний асфальтобетона по ГОСТ 58406.1-2020"""
    sample = models.OneToOneField(TestSample, on_delete=models.CASCADE, related_name='asphalt_test_result')
    
    # === ИЗМЕРЕНИЯ ПЛОТНОСТИ ===
    # Образец 1
    density_1_number = models.CharField(max_length=50, blank=True, verbose_name="№ образца 1")
    density_1_air = models.FloatField(null=True, blank=True, verbose_name="g (на воздухе) 1")
    density_1_water = models.FloatField(null=True, blank=True, verbose_name="g1 (4 мин. в воде) 1")
    density_1_diff_g2g1 = models.FloatField(null=True, blank=True, verbose_name="g2-g1 образец 1")
    density_1_air_after_water = models.FloatField(null=True, blank=True, verbose_name="g2 (на воздухе пос. воды) 1")
    density_1_density = models.FloatField(null=True, blank=True, verbose_name="ρ образец 1")
    
    # Образец 2
    density_2_number = models.CharField(max_length=50, blank=True, verbose_name="№ образца 2")
    density_2_air = models.FloatField(null=True, blank=True, verbose_name="g (на воздухе) 2")
    density_2_water = models.FloatField(null=True, blank=True, verbose_name="g1 (4 мин. в воде) 2")
    density_2_diff_g2g1 = models.FloatField(null=True, blank=True, verbose_name="g2-g1 образец 2")
    density_2_air_after_water = models.FloatField(null=True, blank=True, verbose_name="g2 (на воздухе пос. воды) 2")
    density_2_density = models.FloatField(null=True, blank=True, verbose_name="ρ образец 2")
    
    # Образец 3
    density_3_number = models.CharField(max_length=50, blank=True, verbose_name="№ образца 3")
    density_3_air = models.FloatField(null=True, blank=True, verbose_name="g (на воздухе) 3")
    density_3_water = models.FloatField(null=True, blank=True, verbose_name="g1 (4 мин. в воде) 3")
    density_3_diff_g2g1 = models.FloatField(null=True, blank=True, verbose_name="g2-g1 образец 3")
    density_3_air_after_water = models.FloatField(null=True, blank=True, verbose_name="g2 (на воздухе пос. воды) 3")
    density_3_density = models.FloatField(null=True, blank=True, verbose_name="ρ образец 3")
    
    # Средние и расчетные значения плотности
    average_density = models.FloatField(null=True, blank=True, verbose_name="ρср")
    max_density = models.FloatField(null=True, blank=True, verbose_name="ρмакс")
    void_volume = models.FloatField(null=True, blank=True, verbose_name="Vпустот")
    void_volume_receipt = models.FloatField(null=True, blank=True, verbose_name="Согласованный состав")
    void_volume_variance = models.FloatField(default=1.2, verbose_name="Допуск ±")
    void_volume_min = models.FloatField(default=2.5, verbose_name="Не менее")
    
    # === ГРАНУЛОМЕТРИЧЕСКИЙ СОСТАВ ===
    # Фракция 31.5
    partition_31_5_weight = models.FloatField(null=True, blank=True, verbose_name="Масса 31.5")
    partition_31_5_cho = models.FloatField(null=True, blank=True, verbose_name="ЧО 31.5")
    partition_31_5_pp = models.FloatField(null=True, blank=True, verbose_name="ПП 31.5")
    partition_31_5_receipt = models.FloatField(null=True, blank=True, verbose_name="Состав 31.5")
    partition_31_5_variance = models.FloatField(null=True, blank=True, verbose_name="Отклонение 31.5")
    
    # Фракция 22.4
    partition_22_4_weight = models.FloatField(null=True, blank=True, verbose_name="Масса 22.4")
    partition_22_4_cho = models.FloatField(null=True, blank=True, verbose_name="ЧО 22.4")
    partition_22_4_pp = models.FloatField(null=True, blank=True, verbose_name="ПП 22.4")
    partition_22_4_receipt = models.FloatField(null=True, blank=True, verbose_name="Состав 22.4")
    partition_22_4_variance = models.FloatField(null=True, blank=True, verbose_name="Отклонение 22.4")
    
    # Фракция 16
    partition_16_weight = models.FloatField(null=True, blank=True, verbose_name="Масса 16")
    partition_16_cho = models.FloatField(null=True, blank=True, verbose_name="ЧО 16")
    partition_16_pp = models.FloatField(null=True, blank=True, verbose_name="ПП 16")
    partition_16_receipt = models.FloatField(null=True, blank=True, verbose_name="Состав 16")
    partition_16_variance = models.FloatField(default=5, verbose_name="Отклонение 16")
    
    # Фракция 11.2
    partition_11_2_weight = models.FloatField(null=True, blank=True, verbose_name="Масса 11.2")
    partition_11_2_cho = models.FloatField(null=True, blank=True, verbose_name="ЧО 11.2")
    partition_11_2_pp = models.FloatField(null=True, blank=True, verbose_name="ПП 11.2")
    partition_11_2_receipt = models.FloatField(null=True, blank=True, verbose_name="Состав 11.2")
    partition_11_2_variance = models.FloatField(null=True, blank=True, verbose_name="Отклонение 11.2")
    
    # Фракция 8
    partition_8_weight = models.FloatField(null=True, blank=True, verbose_name="Масса 8")
    partition_8_cho = models.FloatField(null=True, blank=True, verbose_name="ЧО 8")
    partition_8_pp = models.FloatField(null=True, blank=True, verbose_name="ПП 8")
    partition_8_receipt = models.FloatField(null=True, blank=True, verbose_name="Состав 8")
    partition_8_variance = models.FloatField(default=5, verbose_name="Отклонение 8")
    
    # Фракция 5.6
    partition_5_6_weight = models.FloatField(null=True, blank=True, verbose_name="Масса 5.6")
    partition_5_6_cho = models.FloatField(null=True, blank=True, verbose_name="ЧО 5.6")
    partition_5_6_pp = models.FloatField(null=True, blank=True, verbose_name="ПП 5.6")
    partition_5_6_receipt = models.FloatField(null=True, blank=True, verbose_name="Состав 5.6")
    partition_5_6_variance = models.FloatField(null=True, blank=True, verbose_name="Отклонение 5.6")
    
    # Фракция 4
    partition_4_weight = models.FloatField(null=True, blank=True, verbose_name="Масса 4")
    partition_4_cho = models.FloatField(null=True, blank=True, verbose_name="ЧО 4")
    partition_4_pp = models.FloatField(null=True, blank=True, verbose_name="ПП 4")
    partition_4_receipt = models.FloatField(null=True, blank=True, verbose_name="Состав 4")
    partition_4_variance = models.FloatField(default=5, verbose_name="Отклонение 4")
    
    # Фракция 2
    partition_2_weight = models.FloatField(null=True, blank=True, verbose_name="Масса 2")
    partition_2_cho = models.FloatField(null=True, blank=True, verbose_name="ЧО 2")
    partition_2_pp = models.FloatField(null=True, blank=True, verbose_name="ПП 2")
    partition_2_receipt = models.FloatField(null=True, blank=True, verbose_name="Состав 2")
    partition_2_variance = models.FloatField(default=4, verbose_name="Отклонение 2")
    
    # Фракция 0.125
    partition_0_125_weight = models.FloatField(null=True, blank=True, verbose_name="Масса 0.125")
    partition_0_125_cho = models.FloatField(null=True, blank=True, verbose_name="ЧО 0.125")
    partition_0_125_pp = models.FloatField(null=True, blank=True, verbose_name="ПП 0.125")
    partition_0_125_receipt = models.FloatField(null=True, blank=True, verbose_name="Состав 0.125")
    partition_0_125_variance = models.FloatField(null=True, blank=True, verbose_name="Отклонение 0.125")
    
    # Фракция 0.063
    partition_0_063_weight = models.FloatField(null=True, blank=True, verbose_name="Масса 0.063")
    partition_0_063_cho = models.FloatField(null=True, blank=True, verbose_name="ЧО 0.063")
    partition_0_063_pp = models.FloatField(null=True, blank=True, verbose_name="ПП 0.063")
    partition_0_063_receipt = models.FloatField(null=True, blank=True, verbose_name="Состав 0.063")
    partition_0_063_variance = models.FloatField(default=3, verbose_name="Отклонение 0.063")
    
    # === МАКСИМАЛЬНАЯ ПЛОТНОСТЬ СМЕСИ ===
    max_mix_density_mix_weight = models.FloatField(null=True, blank=True, verbose_name="Масса смеси")
    max_mix_density_after_vacuum = models.FloatField(null=True, blank=True, verbose_name="Масса смеси и чаши в воде после вакуума")
    max_mix_density_plate_weight = models.FloatField(null=True, blank=True, verbose_name="Масса чаши в воде")
    
    # === СОДЕРЖАНИЕ ВЯЖУЩЕГО ===
    viscous_tigle_weight = models.FloatField(null=True, blank=True, verbose_name="Масса тигеля")
    viscous_mix_tigle_before = models.FloatField(null=True, blank=True, verbose_name="Масса смеси + тигель до выжигания")
    viscous_mix_tigle_after = models.FloatField(null=True, blank=True, verbose_name="Масса смеси + тигель после выжигания")
    viscous_bitumen_content = models.FloatField(null=True, blank=True, verbose_name="Содержание битума %")
    viscous_bitumen_receipt = models.FloatField(null=True, blank=True, verbose_name="Согласованный состав битума")
    viscous_bitumen_variance = models.FloatField(default=0.4, verbose_name="Допуск битума ±")
    
    # === СТЕКАНИЕ ВЯЖУЩЕГО ===
    binder_empty_glass = models.FloatField(null=True, blank=True, verbose_name="Масса пустого стакана")
    binder_full_glass = models.FloatField(null=True, blank=True, verbose_name="Масса стакана со смесью")
    binder_glass_after = models.FloatField(null=True, blank=True, verbose_name="Масса стакана после удаления смеси")
    binder_trickling = models.FloatField(null=True, blank=True, verbose_name="Стекание вяжущего %")
    binder_max_trickling = models.FloatField(default=0.2, verbose_name="Максимальное стекание")
    
    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Результаты асфальтобетона {self.sample.sample_number}"
    
    class Meta:
        verbose_name = "Результат испытания асфальтобетона"
        verbose_name_plural = "Результаты испытаний асфальтобетона"


class AsphaltCoreTestResult(models.Model):
    """Модель для хранения результатов испытаний кернов из асфальтобетона"""
    
    LAYER_TYPES = [
        ('bottom_coating', 'Низ покрытия'),
        ('base', 'Основание'),
        ('top_coating', 'Верх покрытия'),
        ('sidewalk', 'Тротуар'),
    ]
    
    sample = models.OneToOneField(
        TestSample,
        on_delete=models.CASCADE,
        related_name='asphalt_core_result'
    )
    
    # Слой 1
    layer1_type = models.CharField(max_length=20, choices=LAYER_TYPES, blank=True, null=True)
    layer1_mix_name = models.CharField(max_length=100, blank=True, null=True)
    
    # Образцы слоя 1
    layer1_sample1_number = models.CharField(max_length=50, blank=True, null=True)
    layer1_sample1_actual_thickness = models.FloatField(blank=True, null=True)
    layer1_sample1_project_thickness = models.FloatField(blank=True, null=True)
    layer1_sample1_g = models.FloatField(blank=True, null=True)
    layer1_sample1_g1 = models.FloatField(blank=True, null=True)
    layer1_sample1_g2 = models.FloatField(blank=True, null=True)
    layer1_sample1_g2g1 = models.FloatField(blank=True, null=True)
    layer1_sample1_density = models.FloatField(blank=True, null=True)
    
    layer1_sample2_number = models.CharField(max_length=50, blank=True, null=True)
    layer1_sample2_actual_thickness = models.FloatField(blank=True, null=True)
    layer1_sample2_project_thickness = models.FloatField(blank=True, null=True)
    layer1_sample2_g = models.FloatField(blank=True, null=True)
    layer1_sample2_g1 = models.FloatField(blank=True, null=True)
    layer1_sample2_g2 = models.FloatField(blank=True, null=True)
    layer1_sample2_g2g1 = models.FloatField(blank=True, null=True)
    layer1_sample2_density = models.FloatField(blank=True, null=True)
    
    layer1_average_density = models.FloatField(blank=True, null=True)
    layer1_max_density = models.FloatField(blank=True, null=True)
    layer1_void_volume = models.FloatField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Результат испытания кернов'
        verbose_name_plural = 'Результаты испытаний кернов'
    
    def __str__(self):
        return f"Керны - {self.sample.sample_number}"


class Crushed32703TestResult(models.Model):
    """Модель для хранения результатов испытаний щебня по ГОСТ 32703-2014 (узкие фракции)"""
    
    sample = models.OneToOneField(
        TestSample,
        on_delete=models.CASCADE,
        related_name='crushed_32703_result'
    )
    
    # Гранулометрический состав
    grain_compound_weight = models.FloatField(blank=True, null=True)
    
    # Массы на ситах (5 фракций: 2D, 1.4D, D, d, d/2)
    sieve_2d_weight = models.FloatField(blank=True, null=True)
    sieve_2d_partial = models.FloatField(blank=True, null=True)
    sieve_2d_full = models.FloatField(blank=True, null=True)
    
    sieve_1_4d_weight = models.FloatField(blank=True, null=True)
    sieve_1_4d_partial = models.FloatField(blank=True, null=True)
    sieve_1_4d_full = models.FloatField(blank=True, null=True)
    
    sieve_d_weight = models.FloatField(blank=True, null=True)
    sieve_d_partial = models.FloatField(blank=True, null=True)
    sieve_d_full = models.FloatField(blank=True, null=True)
    
    sieve_d_small_weight = models.FloatField(blank=True, null=True)
    sieve_d_small_partial = models.FloatField(blank=True, null=True)
    sieve_d_small_full = models.FloatField(blank=True, null=True)
    
    sieve_d_2_weight = models.FloatField(blank=True, null=True)
    sieve_d_2_partial = models.FloatField(blank=True, null=True)
    sieve_d_2_full = models.FloatField(blank=True, null=True)
    
    # Марка по проходам через сито
    mark_type = models.CharField(max_length=50, blank=True, null=True)
    
    # Лещадность (одна проба)
    flakiness_weight = models.FloatField(blank=True, null=True)
    flakiness_flaky_weight = models.FloatField(blank=True, null=True)
    flakiness_value = models.FloatField(blank=True, null=True)
    flakiness_mark = models.CharField(max_length=50, blank=True, null=True)
    
    # Дробимость (одна проба)
    crushability_type = models.IntegerField(default=0)  # 0 - изверженные, 1 - осадочные
    crushability_weight = models.FloatField(blank=True, null=True)
    crushability_after_weight = models.FloatField(blank=True, null=True)
    crushability_value = models.FloatField(blank=True, null=True)
    crushability_mark = models.CharField(max_length=50, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Результат испытания щебня по ГОСТ 32703-2014'
        verbose_name_plural = 'Результаты испытаний щебня по ГОСТ 32703-2014'
    
    def __str__(self):
        return f"Щебень 32703 - {self.sample.sample_number}"


class ShchPS70458TestResult(models.Model):
    """Модель для хранения результатов испытаний щебня по ГОСТ 70458-2022"""
    
    sample = models.OneToOneField(
        TestSample,
        on_delete=models.CASCADE,
        related_name='shchps_70458_result'
    )
    
    # Масса пробы для гранулометрического состава
    grain_compound_weight = models.FloatField(blank=True, null=True)
    
    # Содержание пылевидных и глинистых частиц (0.063 сито)
    dust_initial_weight = models.FloatField(blank=True, null=True)
    dust_after_weight = models.FloatField(blank=True, null=True)
    dust_clay_content = models.FloatField(blank=True, null=True)
    
    # Гранулометрический состав (9 фракций)
    # 22.4 мм
    sieve_22_4_weight = models.FloatField(blank=True, null=True)
    sieve_22_4_partial = models.FloatField(blank=True, null=True)
    sieve_22_4_full = models.FloatField(blank=True, null=True)
    
    # 16 мм
    sieve_16_weight = models.FloatField(blank=True, null=True)
    sieve_16_partial = models.FloatField(blank=True, null=True)
    sieve_16_full = models.FloatField(blank=True, null=True)
    
    # 11.2 мм
    sieve_11_2_weight = models.FloatField(blank=True, null=True)
    sieve_11_2_partial = models.FloatField(blank=True, null=True)
    sieve_11_2_full = models.FloatField(blank=True, null=True)
    
    # 8 мм
    sieve_8_weight = models.FloatField(blank=True, null=True)
    sieve_8_partial = models.FloatField(blank=True, null=True)
    sieve_8_full = models.FloatField(blank=True, null=True)
    
    # 5.6 мм
    sieve_5_6_weight = models.FloatField(blank=True, null=True)
    sieve_5_6_partial = models.FloatField(blank=True, null=True)
    sieve_5_6_full = models.FloatField(blank=True, null=True)
    
    # 4 мм
    sieve_4_weight = models.FloatField(blank=True, null=True)
    sieve_4_partial = models.FloatField(blank=True, null=True)
    sieve_4_full = models.FloatField(blank=True, null=True)
    
    # 2 мм
    sieve_2_weight = models.FloatField(blank=True, null=True)
    sieve_2_partial = models.FloatField(blank=True, null=True)
    sieve_2_full = models.FloatField(blank=True, null=True)
    
    # 1 мм
    sieve_1_weight = models.FloatField(blank=True, null=True)
    sieve_1_partial = models.FloatField(blank=True, null=True)
    sieve_1_full = models.FloatField(blank=True, null=True)
    
    # 0.5 мм
    sieve_0_5_weight = models.FloatField(blank=True, null=True)
    sieve_0_5_partial = models.FloatField(blank=True, null=True)
    sieve_0_5_full = models.FloatField(blank=True, null=True)
    
    # Категория и марка
    category_and_mark = models.CharField(max_length=50, blank=True, null=True)
    
    # Лещадность (2 фракции)
    flakiness_4_8_initial = models.FloatField(blank=True, null=True)
    flakiness_4_8_flaky = models.FloatField(blank=True, null=True)
    flakiness_4_8_value = models.FloatField(blank=True, null=True)
    
    flakiness_8_16_initial = models.FloatField(blank=True, null=True)
    flakiness_8_16_flaky = models.FloatField(blank=True, null=True)
    flakiness_8_16_value = models.FloatField(blank=True, null=True)
    
    flakiness_average = models.FloatField(blank=True, null=True)
    flakiness_mark = models.CharField(max_length=50, blank=True, null=True)
    
    # Дробимость (2 фракции)
    crushability_type = models.IntegerField(default=0)  # 0 - изверженные, 1 - осадочные
    
    crushability_4_8_initial = models.FloatField(blank=True, null=True)
    crushability_4_8_after = models.FloatField(blank=True, null=True)
    crushability_4_8_value = models.FloatField(blank=True, null=True)
    
    crushability_8_16_initial = models.FloatField(blank=True, null=True)
    crushability_8_16_after = models.FloatField(blank=True, null=True)
    crushability_8_16_value = models.FloatField(blank=True, null=True)
    
    crushability_average = models.FloatField(blank=True, null=True)
    crushability_mark = models.CharField(max_length=50, blank=True, null=True)
    
    # Насыпная плотность
    bulk_density_1_volume = models.FloatField(blank=True, null=True)
    bulk_density_1_empty = models.FloatField(blank=True, null=True)
    bulk_density_1_weight = models.FloatField(blank=True, null=True)
    bulk_density_1_density = models.FloatField(blank=True, null=True)
    
    bulk_density_2_volume = models.FloatField(blank=True, null=True)
    bulk_density_2_empty = models.FloatField(blank=True, null=True)
    bulk_density_2_weight = models.FloatField(blank=True, null=True)
    bulk_density_2_density = models.FloatField(blank=True, null=True)
    
    bulk_density_average = models.FloatField(blank=True, null=True)
    
    # Содержание глины в комках
    clay_initial_weight = models.FloatField(blank=True, null=True)
    clay_weight = models.FloatField(blank=True, null=True)
    clay_content = models.FloatField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Результат испытания щебня по ГОСТ 70458-2022'
        verbose_name_plural = 'Результаты испытаний щебня по ГОСТ 70458-2022'
    
    def __str__(self):
        return f"Щебень 70458 - {self.sample.sample_number}"


class Crushed8267TestResult(models.Model):
    """Модель для хранения результатов испытаний щебня по ГОСТ 8267-93"""
    
    sample = models.OneToOneField(
        TestSample,
        on_delete=models.CASCADE,
        related_name='crushed_8267_result'
    )
    
    # === ГРАНУЛОМЕТРИЧЕСКИЙ СОСТАВ ===
    grain_compound_weight = models.FloatField(blank=True, null=True, verbose_name="Масса пробы, г")
    
    # Партиции с относительными размерами (универсальный подход)
    # Partition 0: 1.25D
    partition_0_weight = models.FloatField(blank=True, null=True)
    partition_0_partial = models.FloatField(blank=True, null=True)  # Частный остаток
    partition_0_passes = models.FloatField(blank=True, null=True)   # Проходы через сито
    
    # Partition 1: D
    partition_1_weight = models.FloatField(blank=True, null=True)
    partition_1_partial = models.FloatField(blank=True, null=True)
    partition_1_passes = models.FloatField(blank=True, null=True)
    
    # Partition 2: (D+d)/2
    partition_2_weight = models.FloatField(blank=True, null=True)
    partition_2_partial = models.FloatField(blank=True, null=True)
    partition_2_passes = models.FloatField(blank=True, null=True)
    
    # Partition 3: d
    partition_3_weight = models.FloatField(blank=True, null=True)
    partition_3_partial = models.FloatField(blank=True, null=True)
    partition_3_passes = models.FloatField(blank=True, null=True)
    
    # Partition 4: d/2
    partition_4_weight = models.FloatField(blank=True, null=True)
    partition_4_partial = models.FloatField(blank=True, null=True)
    partition_4_passes = models.FloatField(blank=True, null=True)
    
    # === СОДЕРЖАНИЕ ПЫЛЕВИДНЫХ И ГЛИНИСТЫХ ЧАСТИЦ ===
    dust_initial_weight = models.FloatField(blank=True, null=True, verbose_name="Масса начальная, г")
    dust_after_weight = models.FloatField(blank=True, null=True, verbose_name="Масса после отмучивания, г")
    dust_content = models.FloatField(blank=True, null=True, verbose_name="Содержание п/г частиц, %")
    
    # === СОДЕРЖАНИЕ ГЛИНЫ В КОМКАХ ===
    clay_initial_weight = models.FloatField(blank=True, null=True, verbose_name="Масса пробы, г")
    clay_weight = models.FloatField(blank=True, null=True, verbose_name="Масса глины в комках, г")
    clay_content = models.FloatField(blank=True, null=True, verbose_name="Содержание глины в комках, %")
    
    # === СОДЕРЖАНИЕ ЗЕРЕН ПЛАСТИНЧАТОЙ (ЛЕЩАДНОЙ) И ИГЛОВАТОЙ ФОРМЫ ===
    flakiness_weight = models.FloatField(blank=True, null=True, verbose_name="Масса пробы, г")
    flakiness_flaky_weight = models.FloatField(blank=True, null=True, verbose_name="Масса лещадных зерен, г")
    flakiness_value = models.FloatField(blank=True, null=True, verbose_name="Лещадность, %")
    flakiness_mark_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Группа щебня по лещадности")
    
    # === ДРОБИМОСТЬ ===
    crushability_type = models.IntegerField(default=0, verbose_name="Вид породы")
    crushability_weight = models.FloatField(blank=True, null=True, verbose_name="Масса пробы, г")
    crushability_after_weight = models.FloatField(blank=True, null=True, verbose_name="Масса после дробления, г")
    crushability_value = models.FloatField(blank=True, null=True, verbose_name="Дробимость, %")
    crushability_mark_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Марка по дробимости")
    
    # === НАСЫПНАЯ ПЛОТНОСТЬ ===
    # Проба 1
    bulk_density_0_volume = models.FloatField(blank=True, null=True)
    bulk_density_0_empty_weight = models.FloatField(blank=True, null=True)
    bulk_density_0_weight = models.FloatField(blank=True, null=True)
    bulk_density_0_density_value = models.FloatField(blank=True, null=True)
    
    # Проба 2
    bulk_density_1_volume = models.FloatField(blank=True, null=True)
    bulk_density_1_empty_weight = models.FloatField(blank=True, null=True)
    bulk_density_1_weight = models.FloatField(blank=True, null=True)
    bulk_density_1_density_value = models.FloatField(blank=True, null=True)
    
    bulk_density_average = models.FloatField(blank=True, null=True, verbose_name="Средняя насыпная плотность")
    
    # === СОДЕРЖАНИЕ ЗЕРЕН СЛАБЫХ ПОРОД ===
    weak_rock_initial_weight = models.FloatField(blank=True, null=True, verbose_name="Масса начальная, гр")
    weak_rock_weight = models.FloatField(blank=True, null=True, verbose_name="Масса слабых зерен, гр")
    weak_rock_content = models.FloatField(blank=True, null=True, verbose_name="Содержание, %")
    
    # === СРЕДНЯЯ ПЛОТНОСТЬ ===
    average_density_dried_weight = models.FloatField(blank=True, null=True, verbose_name="Масса высушенной пробы, гр")
    average_density_weight_in_air = models.FloatField(blank=True, null=True, verbose_name="Масса в насыщенном состоянии на воздухе, гр")
    average_density_weight_in_water = models.FloatField(blank=True, null=True, verbose_name="Масса корзины и пробы в воде, гр")
    average_density_empty_basket_weight = models.FloatField(blank=True, null=True, verbose_name="Масса пустой корзины, гр")
    average_density_value = models.FloatField(blank=True, null=True, verbose_name="Средняя плотность")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Результат испытания щебня по ГОСТ 8267-93'
        verbose_name_plural = 'Результаты испытаний щебня по ГОСТ 8267-93'
    
    def __str__(self):
        return f"Щебень 8267 - {self.sample.sample_number}"


class ShchPSTestResult(models.Model):
    """Модель для хранения результатов испытаний ЩПС по ГОСТ 25607-2009"""
    
    sample = models.OneToOneField(
        TestSample,
        on_delete=models.CASCADE,
        related_name='shchps_result'
    )
    
    # Содержание пылевидных и глинистых частиц
    dust_initial_weight = models.FloatField(blank=True, null=True, verbose_name="Масса начальная")
    dust_after_wash_weight = models.FloatField(blank=True, null=True, verbose_name="Масса после промывки")
    dust_clay_content = models.FloatField(blank=True, null=True, verbose_name="Содержание п/г, %")
    
    # Зерновой состав (фракции) - 8 фракций
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
    
    # 2.5 мм
    sieve_2_5_weight = models.FloatField(blank=True, null=True)
    sieve_2_5_partial = models.FloatField(blank=True, null=True)
    sieve_2_5_full = models.FloatField(blank=True, null=True)
    
    # 0.63 мм
    sieve_0_63_weight = models.FloatField(blank=True, null=True)
    sieve_0_63_partial = models.FloatField(blank=True, null=True)
    sieve_0_63_full = models.FloatField(blank=True, null=True)
    
    # 0.16 мм
    sieve_0_16_weight = models.FloatField(blank=True, null=True)
    sieve_0_16_partial = models.FloatField(blank=True, null=True)
    sieve_0_16_full = models.FloatField(blank=True, null=True)
    
    # 0.05 мм
    sieve_0_05_weight = models.FloatField(blank=True, null=True)
    sieve_0_05_partial = models.FloatField(blank=True, null=True)
    sieve_0_05_full = models.FloatField(blank=True, null=True)
    
    # Дробимость (4 фракции)
    fragility_40_70_initial = models.FloatField(blank=True, null=True)
    fragility_40_70_after = models.FloatField(blank=True, null=True)
    fragility_40_70_value = models.FloatField(blank=True, null=True)
    
    fragility_20_40_initial = models.FloatField(blank=True, null=True)
    fragility_20_40_after = models.FloatField(blank=True, null=True)
    fragility_20_40_value = models.FloatField(blank=True, null=True)
    
    fragility_10_20_initial = models.FloatField(blank=True, null=True)
    fragility_10_20_after = models.FloatField(blank=True, null=True)
    fragility_10_20_value = models.FloatField(blank=True, null=True)
    
    fragility_5_10_initial = models.FloatField(blank=True, null=True)
    fragility_5_10_after = models.FloatField(blank=True, null=True)
    fragility_5_10_value = models.FloatField(blank=True, null=True)
    
    fragility_summary = models.FloatField(blank=True, null=True)
    
    # Лещадность (4 фракции)
    flakiness_40_70_initial = models.FloatField(blank=True, null=True)
    flakiness_40_70_flaky = models.FloatField(blank=True, null=True)
    flakiness_40_70_value = models.FloatField(blank=True, null=True)
    
    flakiness_20_40_initial = models.FloatField(blank=True, null=True)
    flakiness_20_40_flaky = models.FloatField(blank=True, null=True)
    flakiness_20_40_value = models.FloatField(blank=True, null=True)
    
    flakiness_10_20_initial = models.FloatField(blank=True, null=True)
    flakiness_10_20_flaky = models.FloatField(blank=True, null=True)
    flakiness_10_20_value = models.FloatField(blank=True, null=True)
    
    flakiness_5_10_initial = models.FloatField(blank=True, null=True)
    flakiness_5_10_flaky = models.FloatField(blank=True, null=True)
    flakiness_5_10_value = models.FloatField(blank=True, null=True)
    
    flakiness_summary = models.FloatField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Результат испытания ЩПС'
        verbose_name_plural = 'Результаты испытаний ЩПС'
    
    def __str__(self):
        return f"ЩПС - {self.sample.sample_number}"
