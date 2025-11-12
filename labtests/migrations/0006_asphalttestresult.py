# Generated manually for AsphaltTestResult model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labtests', '0005_testresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsphaltTestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Плотность - 3 образца
                ('density_1_number', models.CharField(blank=True, max_length=50, verbose_name='№ образца 1')),
                ('density_1_air', models.FloatField(blank=True, null=True, verbose_name='g (на воздухе) 1')),
                ('density_1_water', models.FloatField(blank=True, null=True, verbose_name='g1 (4 мин. в воде) 1')),
                ('density_1_diff_g2g1', models.FloatField(blank=True, null=True, verbose_name='g2-g1 образец 1')),
                ('density_1_air_after_water', models.FloatField(blank=True, null=True, verbose_name='g2 (на воздухе пос. воды) 1')),
                ('density_1_density', models.FloatField(blank=True, null=True, verbose_name='ρ образец 1')),
                
                ('density_2_number', models.CharField(blank=True, max_length=50, verbose_name='№ образца 2')),
                ('density_2_air', models.FloatField(blank=True, null=True, verbose_name='g (на воздухе) 2')),
                ('density_2_water', models.FloatField(blank=True, null=True, verbose_name='g1 (4 мин. в воде) 2')),
                ('density_2_diff_g2g1', models.FloatField(blank=True, null=True, verbose_name='g2-g1 образец 2')),
                ('density_2_air_after_water', models.FloatField(blank=True, null=True, verbose_name='g2 (на воздухе пос. воды) 2')),
                ('density_2_density', models.FloatField(blank=True, null=True, verbose_name='ρ образец 2')),
                
                ('density_3_number', models.CharField(blank=True, max_length=50, verbose_name='№ образца 3')),
                ('density_3_air', models.FloatField(blank=True, null=True, verbose_name='g (на воздухе) 3')),
                ('density_3_water', models.FloatField(blank=True, null=True, verbose_name='g1 (4 мин. в воде) 3')),
                ('density_3_diff_g2g1', models.FloatField(blank=True, null=True, verbose_name='g2-g1 образец 3')),
                ('density_3_air_after_water', models.FloatField(blank=True, null=True, verbose_name='g2 (на воздухе пос. воды) 3')),
                ('density_3_density', models.FloatField(blank=True, null=True, verbose_name='ρ образец 3')),
                
                # Средние значения
                ('average_density', models.FloatField(blank=True, null=True, verbose_name='ρср')),
                ('max_density', models.FloatField(blank=True, null=True, verbose_name='ρмакс')),
                ('void_volume', models.FloatField(blank=True, null=True, verbose_name='Vпустот')),
                ('void_volume_receipt', models.FloatField(blank=True, null=True, verbose_name='Согласованный состав')),
                ('void_volume_variance', models.FloatField(default=1.2, verbose_name='Допуск ±')),
                ('void_volume_min', models.FloatField(default=2.5, verbose_name='Не менее')),
                
                # Гранулометрический состав
                ('partition_31_5_weight', models.FloatField(blank=True, null=True, verbose_name='Масса 31.5')),
                ('partition_31_5_cho', models.FloatField(blank=True, null=True, verbose_name='ЧО 31.5')),
                ('partition_31_5_pp', models.FloatField(blank=True, null=True, verbose_name='ПП 31.5')),
                ('partition_31_5_receipt', models.FloatField(blank=True, null=True, verbose_name='Состав 31.5')),
                ('partition_31_5_variance', models.FloatField(blank=True, null=True, verbose_name='Отклонение 31.5')),
                
                ('partition_22_4_weight', models.FloatField(blank=True, null=True, verbose_name='Масса 22.4')),
                ('partition_22_4_cho', models.FloatField(blank=True, null=True, verbose_name='ЧО 22.4')),
                ('partition_22_4_pp', models.FloatField(blank=True, null=True, verbose_name='ПП 22.4')),
                ('partition_22_4_receipt', models.FloatField(blank=True, null=True, verbose_name='Состав 22.4')),
                ('partition_22_4_variance', models.FloatField(blank=True, null=True, verbose_name='Отклонение 22.4')),
                
                ('partition_16_weight', models.FloatField(blank=True, null=True, verbose_name='Масса 16')),
                ('partition_16_cho', models.FloatField(blank=True, null=True, verbose_name='ЧО 16')),
                ('partition_16_pp', models.FloatField(blank=True, null=True, verbose_name='ПП 16')),
                ('partition_16_receipt', models.FloatField(blank=True, null=True, verbose_name='Состав 16')),
                ('partition_16_variance', models.FloatField(default=5, verbose_name='Отклонение 16')),
                
                ('partition_11_2_weight', models.FloatField(blank=True, null=True, verbose_name='Масса 11.2')),
                ('partition_11_2_cho', models.FloatField(blank=True, null=True, verbose_name='ЧО 11.2')),
                ('partition_11_2_pp', models.FloatField(blank=True, null=True, verbose_name='ПП 11.2')),
                ('partition_11_2_receipt', models.FloatField(blank=True, null=True, verbose_name='Состав 11.2')),
                ('partition_11_2_variance', models.FloatField(blank=True, null=True, verbose_name='Отклонение 11.2')),
                
                ('partition_8_weight', models.FloatField(blank=True, null=True, verbose_name='Масса 8')),
                ('partition_8_cho', models.FloatField(blank=True, null=True, verbose_name='ЧО 8')),
                ('partition_8_pp', models.FloatField(blank=True, null=True, verbose_name='ПП 8')),
                ('partition_8_receipt', models.FloatField(blank=True, null=True, verbose_name='Состав 8')),
                ('partition_8_variance', models.FloatField(default=5, verbose_name='Отклонение 8')),
                
                ('partition_5_6_weight', models.FloatField(blank=True, null=True, verbose_name='Масса 5.6')),
                ('partition_5_6_cho', models.FloatField(blank=True, null=True, verbose_name='ЧО 5.6')),
                ('partition_5_6_pp', models.FloatField(blank=True, null=True, verbose_name='ПП 5.6')),
                ('partition_5_6_receipt', models.FloatField(blank=True, null=True, verbose_name='Состав 5.6')),
                ('partition_5_6_variance', models.FloatField(blank=True, null=True, verbose_name='Отклонение 5.6')),
                
                ('partition_4_weight', models.FloatField(blank=True, null=True, verbose_name='Масса 4')),
                ('partition_4_cho', models.FloatField(blank=True, null=True, verbose_name='ЧО 4')),
                ('partition_4_pp', models.FloatField(blank=True, null=True, verbose_name='ПП 4')),
                ('partition_4_receipt', models.FloatField(blank=True, null=True, verbose_name='Состав 4')),
                ('partition_4_variance', models.FloatField(default=5, verbose_name='Отклонение 4')),
                
                ('partition_2_weight', models.FloatField(blank=True, null=True, verbose_name='Масса 2')),
                ('partition_2_cho', models.FloatField(blank=True, null=True, verbose_name='ЧО 2')),
                ('partition_2_pp', models.FloatField(blank=True, null=True, verbose_name='ПП 2')),
                ('partition_2_receipt', models.FloatField(blank=True, null=True, verbose_name='Состав 2')),
                ('partition_2_variance', models.FloatField(default=4, verbose_name='Отклонение 2')),
                
                ('partition_0_125_weight', models.FloatField(blank=True, null=True, verbose_name='Масса 0.125')),
                ('partition_0_125_cho', models.FloatField(blank=True, null=True, verbose_name='ЧО 0.125')),
                ('partition_0_125_pp', models.FloatField(blank=True, null=True, verbose_name='ПП 0.125')),
                ('partition_0_125_receipt', models.FloatField(blank=True, null=True, verbose_name='Состав 0.125')),
                ('partition_0_125_variance', models.FloatField(blank=True, null=True, verbose_name='Отклонение 0.125')),
                
                ('partition_0_063_weight', models.FloatField(blank=True, null=True, verbose_name='Масса 0.063')),
                ('partition_0_063_cho', models.FloatField(blank=True, null=True, verbose_name='ЧО 0.063')),
                ('partition_0_063_pp', models.FloatField(blank=True, null=True, verbose_name='ПП 0.063')),
                ('partition_0_063_receipt', models.FloatField(blank=True, null=True, verbose_name='Состав 0.063')),
                ('partition_0_063_variance', models.FloatField(default=3, verbose_name='Отклонение 0.063')),
                
                # Максимальная плотность смеси
                ('max_mix_density_mix_weight', models.FloatField(blank=True, null=True, verbose_name='Масса смеси')),
                ('max_mix_density_after_vacuum', models.FloatField(blank=True, null=True, verbose_name='Масса смеси и чаши в воде после вакуума')),
                ('max_mix_density_plate_weight', models.FloatField(blank=True, null=True, verbose_name='Масса чаши в воде')),
                
                # Содержание вяжущего
                ('viscous_tigle_weight', models.FloatField(blank=True, null=True, verbose_name='Масса тигеля')),
                ('viscous_mix_tigle_before', models.FloatField(blank=True, null=True, verbose_name='Масса смеси + тигель до выжигания')),
                ('viscous_mix_tigle_after', models.FloatField(blank=True, null=True, verbose_name='Масса смеси + тигель после выжигания')),
                ('viscous_bitumen_content', models.FloatField(blank=True, null=True, verbose_name='Содержание битума %')),
                ('viscous_bitumen_receipt', models.FloatField(blank=True, null=True, verbose_name='Согласованный состав битума')),
                ('viscous_bitumen_variance', models.FloatField(default=0.4, verbose_name='Допуск битума ±')),
                
                # Стекание вяжущего
                ('binder_empty_glass', models.FloatField(blank=True, null=True, verbose_name='Масса пустого стакана')),
                ('binder_full_glass', models.FloatField(blank=True, null=True, verbose_name='Масса стакана со смесью')),
                ('binder_glass_after', models.FloatField(blank=True, null=True, verbose_name='Масса стакана после удаления смеси')),
                ('binder_trickling', models.FloatField(blank=True, null=True, verbose_name='Стекание вяжущего %')),
                ('binder_max_trickling', models.FloatField(default=0.2, verbose_name='Максимальное стекание')),
                
                # Метаданные
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                
                # Связь с образцом
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='asphalt_test_result', to='labtests.testsample')),
            ],
            options={
                'verbose_name': 'Результат испытания асфальтобетона',
                'verbose_name_plural': 'Результаты испытаний асфальтобетона',
            },
        ),
    ]
