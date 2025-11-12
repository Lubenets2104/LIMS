# Generated migration for EmulsionTestResult model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labtests', '0014_update_bitumen_normatives'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmulsionTestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                
                # Внешний вид
                ('appearance', models.CharField(blank=True, max_length=100, null=True, verbose_name='Внешний вид')),
                
                # Условная вязкость
                ('viscosity_time', models.FloatField(blank=True, null=True, verbose_name='Время истечения, с')),
                ('viscosity_value', models.FloatField(blank=True, null=True, verbose_name='Условная вязкость')),
                ('viscosity_min', models.FloatField(default=10, verbose_name='Минимум')),
                ('viscosity_max', models.FloatField(default=50, verbose_name='Максимум')),
                
                # pH
                ('ph_value', models.FloatField(blank=True, null=True, verbose_name='pH')),
                ('ph_min', models.FloatField(default=2, verbose_name='Минимум pH')),
                ('ph_max', models.FloatField(default=7, verbose_name='Максимум pH')),
                
                # Массовая доля остатка на сите №0.8
                ('sieve_08_container_weight', models.FloatField(blank=True, null=True, verbose_name='Масса бюксы')),
                ('sieve_08_container_with_residue', models.FloatField(blank=True, null=True, verbose_name='Масса бюксы с остатком')),
                ('sieve_08_emulsion_weight', models.FloatField(blank=True, null=True, verbose_name='Масса эмульсии')),
                ('sieve_08_residue_percent', models.FloatField(blank=True, null=True, verbose_name='Массовая доля остатка %')),
                ('sieve_08_max', models.FloatField(default=0.08, verbose_name='Максимум')),
                
                # Массовая доля остатка на сите №0.14
                ('sieve_014_container_weight', models.FloatField(blank=True, null=True, verbose_name='Масса бюксы')),
                ('sieve_014_container_with_residue', models.FloatField(blank=True, null=True, verbose_name='Масса бюксы с остатком')),
                ('sieve_014_emulsion_weight', models.FloatField(blank=True, null=True, verbose_name='Масса эмульсии')),
                ('sieve_014_residue_percent', models.FloatField(blank=True, null=True, verbose_name='Массовая доля остатка %')),
                ('sieve_014_max', models.FloatField(default=0.2, verbose_name='Максимум')),
                
                # Массовая доля вяжущего с эмульгатором
                ('binder_1_container_weight', models.FloatField(blank=True, null=True, verbose_name='Масса чашки 1')),
                ('binder_1_emulsion_before', models.FloatField(blank=True, null=True, verbose_name='Масса эмульсии до выпаривания 1')),
                ('binder_1_after_evaporation', models.FloatField(blank=True, null=True, verbose_name='Масса после выпаривания 1')),
                ('binder_1_content', models.FloatField(blank=True, null=True, verbose_name='Массовая доля вяжущего 1, %')),
                
                ('binder_2_container_weight', models.FloatField(blank=True, null=True, verbose_name='Масса чашки 2')),
                ('binder_2_emulsion_before', models.FloatField(blank=True, null=True, verbose_name='Масса эмульсии до выпаривания 2')),
                ('binder_2_after_evaporation', models.FloatField(blank=True, null=True, verbose_name='Масса после выпаривания 2')),
                ('binder_2_content', models.FloatField(blank=True, null=True, verbose_name='Массовая доля вяжущего 2, %')),
                
                ('binder_average', models.FloatField(blank=True, null=True, verbose_name='Средняя массовая доля вяжущего, %')),
                ('binder_min', models.FloatField(default=50, verbose_name='Минимум')),
                ('binder_max', models.FloatField(default=60, verbose_name='Максимум')),
                
                # Устойчивость при хранении - 7 суток
                ('stability_7_container_weight', models.FloatField(blank=True, null=True, verbose_name='Масса стакана')),
                ('stability_7_sample_weight', models.FloatField(blank=True, null=True, verbose_name='Масса пробы эмульсии')),
                ('stability_7_residue_weight', models.FloatField(blank=True, null=True, verbose_name='Масса остатка на сите')),
                ('stability_7_percent', models.FloatField(blank=True, null=True, verbose_name='Устойчивость 7 суток, %')),
                ('stability_7_max', models.FloatField(default=0.5, verbose_name='Максимум')),
                
                # Устойчивость при хранении - 30 суток
                ('stability_30_container_weight', models.FloatField(blank=True, null=True, verbose_name='Масса стакана')),
                ('stability_30_sample_weight', models.FloatField(blank=True, null=True, verbose_name='Масса пробы эмульсии')),
                ('stability_30_residue_weight', models.FloatField(blank=True, null=True, verbose_name='Масса остатка на сите')),
                ('stability_30_percent', models.FloatField(blank=True, null=True, verbose_name='Устойчивость 30 суток, %')),
                ('stability_30_max', models.FloatField(default=1, verbose_name='Максимум')),
                
                # Устойчивость к перемешиванию
                ('mixing_container_weight', models.FloatField(blank=True, null=True, verbose_name='Масса стакана')),
                ('mixing_sample_weight', models.FloatField(blank=True, null=True, verbose_name='Масса пробы эмульсии')),
                ('mixing_residue_weight', models.FloatField(blank=True, null=True, verbose_name='Масса остатка на сите')),
                ('mixing_stability_percent', models.FloatField(blank=True, null=True, verbose_name='Устойчивость к перемешиванию, %')),
                ('mixing_stability_max', models.FloatField(default=0.5, verbose_name='Максимум')),
                
                # Устойчивость при транспортировании
                ('transport_stability', models.CharField(blank=True, max_length=100, null=True, verbose_name='Устойчивость при транспортировании')),
                
                # Сцепление с минеральными материалами
                ('adhesion', models.CharField(blank=True, max_length=100, null=True, verbose_name='Сцепление')),
                ('adhesion_norm', models.CharField(default='полное покрытие поверхности, не смывается', max_length=100, verbose_name='Норматив')),
                
                # Глубина проникания иглы в остаток
                ('needle_penetration_1', models.FloatField(blank=True, null=True, verbose_name='Глубина проникания 1, 0.1 мм')),
                ('needle_penetration_2', models.FloatField(blank=True, null=True, verbose_name='Глубина проникания 2, 0.1 мм')),
                ('needle_penetration_3', models.FloatField(blank=True, null=True, verbose_name='Глубина проникания 3, 0.1 мм')),
                ('needle_penetration_average', models.FloatField(blank=True, null=True, verbose_name='Среднее значение, 0.1 мм')),
                ('needle_penetration_min', models.FloatField(default=60, verbose_name='Минимум')),
                ('needle_penetration_max', models.FloatField(default=130, verbose_name='Максимум')),
                
                # Температура размягчения остатка
                ('softening_temp_1', models.FloatField(blank=True, null=True, verbose_name='Температура размягчения 1, °C')),
                ('softening_temp_2', models.FloatField(blank=True, null=True, verbose_name='Температура размягчения 2, °C')),
                ('softening_temp_average', models.FloatField(blank=True, null=True, verbose_name='Средняя температура, °C')),
                ('softening_temp_min', models.FloatField(default=47, verbose_name='Минимум')),
                
                # Эластичность остатка при 25°С
                ('elasticity_1', models.FloatField(blank=True, null=True, verbose_name='Эластичность 1, см')),
                ('elasticity_2', models.FloatField(blank=True, null=True, verbose_name='Эластичность 2, см')),
                ('elasticity_3', models.FloatField(blank=True, null=True, verbose_name='Эластичность 3, см')),
                ('elasticity_average', models.FloatField(blank=True, null=True, verbose_name='Среднее значение, см')),
                ('elasticity_min', models.FloatField(default=80, verbose_name='Минимум')),
                
                # Дополнительные поля
                ('test_date', models.DateField(blank=True, null=True, verbose_name='Дата испытания')),
                ('tester_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='ФИО испытателя')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Примечания')),
                
                # Метаданные
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                
                # Связь с образцом
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='emulsion_result', to='labtests.testsample')),
            ],
            options={
                'verbose_name': 'Результат испытания эмульсии',
                'verbose_name_plural': 'Результаты испытаний эмульсии',
            },
        ),
    ]
