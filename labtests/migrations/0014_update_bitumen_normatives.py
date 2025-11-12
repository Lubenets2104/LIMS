# Generated manually for updating BitumenTestResult33133 model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labtests', '0013_bitumentestresult33133'),
    ]

    operations = [
        # Изменяем поля нормативов - убираем значения по умолчанию
        migrations.AlterField(
            model_name='bitumentestresult33133',
            name='needle_deep_min',
            field=models.FloatField(blank=True, null=True, verbose_name='Минимальная глубина проникания (норма)'),
        ),
        migrations.AlterField(
            model_name='bitumentestresult33133',
            name='needle_deep_max',
            field=models.FloatField(blank=True, null=True, verbose_name='Максимальная глубина проникания (норма)'),
        ),
        migrations.AlterField(
            model_name='bitumentestresult33133',
            name='softening_temperature_min',
            field=models.FloatField(blank=True, null=True, verbose_name='Минимальная температура размягчения (норма)'),
        ),
        migrations.AlterField(
            model_name='bitumentestresult33133',
            name='extensibility_min',
            field=models.FloatField(blank=True, null=True, verbose_name='Минимальная растяжимость (норма)'),
        ),
        migrations.AlterField(
            model_name='bitumentestresult33133',
            name='fragility_temperature_max',
            field=models.FloatField(blank=True, null=True, verbose_name='Максимальная температура хрупкости (норма)'),
        ),
        migrations.AlterField(
            model_name='bitumentestresult33133',
            name='flash_temperature_min',
            field=models.FloatField(blank=True, null=True, verbose_name='Минимальная температура вспышки (норма)'),
        ),
        migrations.AlterField(
            model_name='bitumentestresult33133',
            name='weight_change_max',
            field=models.FloatField(blank=True, null=True, verbose_name='Максимальное изменение массы (норма)'),
        ),
        migrations.AlterField(
            model_name='bitumentestresult33133',
            name='softening_temperature_change_max',
            field=models.FloatField(blank=True, null=True, verbose_name='Максимальное изменение температуры (норма)'),
        ),
    ]
