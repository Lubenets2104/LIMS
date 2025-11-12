# Generated manually on 2025-08-15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labtests', '0009_crushed32703testresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crushed8267TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grain_compound_weight', models.FloatField(blank=True, null=True, verbose_name='Масса пробы, г')),
                
                # Гранулометрический состав - 70 мм
                ('sieve_70_weight', models.FloatField(blank=True, null=True)),
                ('sieve_70_partial', models.FloatField(blank=True, null=True)),
                ('sieve_70_full', models.FloatField(blank=True, null=True)),
                
                # 40 мм
                ('sieve_40_weight', models.FloatField(blank=True, null=True)),
                ('sieve_40_partial', models.FloatField(blank=True, null=True)),
                ('sieve_40_full', models.FloatField(blank=True, null=True)),
                
                # 20 мм
                ('sieve_20_weight', models.FloatField(blank=True, null=True)),
                ('sieve_20_partial', models.FloatField(blank=True, null=True)),
                ('sieve_20_full', models.FloatField(blank=True, null=True)),
                
                # 10 мм
                ('sieve_10_weight', models.FloatField(blank=True, null=True)),
                ('sieve_10_partial', models.FloatField(blank=True, null=True)),
                ('sieve_10_full', models.FloatField(blank=True, null=True)),
                
                # 5 мм
                ('sieve_5_weight', models.FloatField(blank=True, null=True)),
                ('sieve_5_partial', models.FloatField(blank=True, null=True)),
                ('sieve_5_full', models.FloatField(blank=True, null=True)),
                
                # 2.5 мм
                ('sieve_2_5_weight', models.FloatField(blank=True, null=True)),
                ('sieve_2_5_partial', models.FloatField(blank=True, null=True)),
                ('sieve_2_5_full', models.FloatField(blank=True, null=True)),
                
                # 1.25 мм
                ('sieve_1_25_weight', models.FloatField(blank=True, null=True)),
                ('sieve_1_25_partial', models.FloatField(blank=True, null=True)),
                ('sieve_1_25_full', models.FloatField(blank=True, null=True)),
                
                # Фракция
                ('fraction_type', models.CharField(blank=True, max_length=50, null=True)),
                
                # Пылевидные и глинистые частицы
                ('dust_initial_weight', models.FloatField(blank=True, null=True)),
                ('dust_after_weight', models.FloatField(blank=True, null=True)),
                ('dust_content', models.FloatField(blank=True, null=True)),
                
                # Глина в комках
                ('clay_initial_weight', models.FloatField(blank=True, null=True)),
                ('clay_weight', models.FloatField(blank=True, null=True)),
                ('clay_content', models.FloatField(blank=True, null=True)),
                
                # Лещадность
                ('flakiness_5_10_weight', models.FloatField(blank=True, null=True)),
                ('flakiness_5_10_flaky_weight', models.FloatField(blank=True, null=True)),
                ('flakiness_5_10_value', models.FloatField(blank=True, null=True)),
                
                ('flakiness_10_20_weight', models.FloatField(blank=True, null=True)),
                ('flakiness_10_20_flaky_weight', models.FloatField(blank=True, null=True)),
                ('flakiness_10_20_value', models.FloatField(blank=True, null=True)),
                
                ('flakiness_20_40_weight', models.FloatField(blank=True, null=True)),
                ('flakiness_20_40_flaky_weight', models.FloatField(blank=True, null=True)),
                ('flakiness_20_40_value', models.FloatField(blank=True, null=True)),
                
                ('flakiness_average', models.FloatField(blank=True, null=True)),
                ('flakiness_group', models.CharField(blank=True, max_length=10, null=True)),
                
                # Дробимость
                ('crushability_type', models.IntegerField(default=0)),
                
                ('crushability_5_10_weight', models.FloatField(blank=True, null=True)),
                ('crushability_5_10_after_weight', models.FloatField(blank=True, null=True)),
                ('crushability_5_10_value', models.FloatField(blank=True, null=True)),
                
                ('crushability_10_20_weight', models.FloatField(blank=True, null=True)),
                ('crushability_10_20_after_weight', models.FloatField(blank=True, null=True)),
                ('crushability_10_20_value', models.FloatField(blank=True, null=True)),
                
                ('crushability_20_40_weight', models.FloatField(blank=True, null=True)),
                ('crushability_20_40_after_weight', models.FloatField(blank=True, null=True)),
                ('crushability_20_40_value', models.FloatField(blank=True, null=True)),
                
                ('crushability_average', models.FloatField(blank=True, null=True)),
                ('crushability_mark', models.CharField(blank=True, max_length=50, null=True)),
                
                # Насыпная плотность
                ('bulk_density_average', models.FloatField(blank=True, null=True)),
                
                # Метаданные
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                
                # Связь с образцом
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='crushed_8267_result', to='labtests.testsample')),
            ],
            options={
                'verbose_name': 'Результат испытания щебня по ГОСТ 8267-93',
                'verbose_name_plural': 'Результаты испытаний щебня по ГОСТ 8267-93',
            },
        ),
    ]
