# Generated manually for BitumenTestResult33133 model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labtests', '0012_rename_bulk_density_0_density_value_crushed8267testresult_crushability_10_20_after_weight_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BitumenTestResult33133',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('needle_deep', models.FloatField(blank=True, null=True, verbose_name='Глубина проникания иглы при 25°С, мм')),
                ('needle_deep_min', models.FloatField(default=131, verbose_name='Минимальная глубина проникания (норма)')),
                ('needle_deep_max', models.FloatField(default=200, verbose_name='Максимальная глубина проникания (норма)')),
                ('softening_temperature', models.FloatField(blank=True, null=True, verbose_name='Температура размягчения, °С')),
                ('softening_temperature_min', models.FloatField(default=42, verbose_name='Минимальная температура размягчения (норма)')),
                ('extensibility', models.FloatField(blank=True, null=True, verbose_name='Растяжимость при 0°С, см')),
                ('extensibility_min', models.FloatField(default=6, verbose_name='Минимальная растяжимость (норма)')),
                ('fragility_temperature', models.FloatField(blank=True, null=True, verbose_name='Температура хрупкости, °С')),
                ('fragility_temperature_max', models.FloatField(default=-21, verbose_name='Максимальная температура хрупкости (норма)')),
                ('flash_temperature', models.FloatField(blank=True, null=True, verbose_name='Температура вспышки, °С')),
                ('flash_temperature_min', models.FloatField(default=220, verbose_name='Минимальная температура вспышки (норма)')),
                ('container_a_weight', models.FloatField(blank=True, null=True, verbose_name='Масса стеклянного контейнера А, г')),
                ('container_a_bitumen_before', models.FloatField(blank=True, null=True, verbose_name='Масса контейнера А с битумом до старения, г')),
                ('container_a_bitumen_after', models.FloatField(blank=True, null=True, verbose_name='Масса контейнера А с битумом после старения, г')),
                ('container_a_result', models.FloatField(blank=True, editable=False, null=True, verbose_name='Результат контейнера А, %')),
                ('container_b_weight', models.FloatField(blank=True, null=True, verbose_name='Масса стеклянного контейнера B, г')),
                ('container_b_bitumen_before', models.FloatField(blank=True, null=True, verbose_name='Масса контейнера B с битумом до старения, г')),
                ('container_b_bitumen_after', models.FloatField(blank=True, null=True, verbose_name='Масса контейнера B с битумом после старения, г')),
                ('container_b_result', models.FloatField(blank=True, editable=False, null=True, verbose_name='Результат контейнера B, %')),
                ('weight_change', models.FloatField(blank=True, editable=False, null=True, verbose_name='Изменение массы после старения, %')),
                ('weight_change_max', models.FloatField(default=0.8, verbose_name='Максимальное изменение массы (норма)')),
                ('softening_temperature_change', models.FloatField(blank=True, null=True, verbose_name='Изменение температуры размягчения после старения, °С')),
                ('softening_temperature_change_max', models.FloatField(default=7, verbose_name='Максимальное изменение температуры (норма)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bitumen_33133_result', to='labtests.testsample')),
            ],
            options={
                'verbose_name': 'Результат испытания битума ГОСТ 33133-2014',
                'verbose_name_plural': 'Результаты испытаний битума ГОСТ 33133-2014',
            },
        ),
    ]
