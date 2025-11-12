# Generated manually on 2025-08-15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labtests', '0010_crushed8267testresult'),
    ]

    operations = [
        # Удаляем старые поля
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_70_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_70_partial',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_70_full',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_40_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_40_partial',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_40_full',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_20_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_20_partial',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_20_full',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_10_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_10_partial',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_10_full',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_5_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_5_partial',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_5_full',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_2_5_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_2_5_partial',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_2_5_full',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_1_25_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_1_25_partial',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='sieve_1_25_full',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='fraction_type',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='flakiness_5_10_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='flakiness_5_10_flaky_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='flakiness_5_10_value',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='flakiness_10_20_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='flakiness_10_20_flaky_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='flakiness_10_20_value',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='flakiness_20_40_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='flakiness_20_40_flaky_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='flakiness_20_40_value',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='flakiness_average',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='flakiness_group',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='crushability_5_10_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='crushability_5_10_after_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='crushability_5_10_value',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='crushability_10_20_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='crushability_10_20_after_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='crushability_10_20_value',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='crushability_20_40_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='crushability_20_40_after_weight',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='crushability_20_40_value',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='crushability_average',
        ),
        migrations.RemoveField(
            model_name='crushed8267testresult',
            name='crushability_mark',
        ),
        
        # Добавляем новые поля
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_0_weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_0_partial',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_0_passes',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_1_weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_1_partial',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_1_passes',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_2_weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_2_partial',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_2_passes',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_3_weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_3_partial',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_3_passes',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_4_weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_4_partial',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='partition_4_passes',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='flakiness_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса пробы, г'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='flakiness_flaky_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса лещадных зерен, г'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='flakiness_value',
            field=models.FloatField(blank=True, null=True, verbose_name='Лещадность, %'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='flakiness_mark_type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Группа щебня по лещадности'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='crushability_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса пробы, г'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='crushability_after_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса после дробления, г'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='crushability_value',
            field=models.FloatField(blank=True, null=True, verbose_name='Дробимость, %'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='crushability_mark_type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Марка по дробимости'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='bulk_density_0_volume',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='bulk_density_0_empty_weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='bulk_density_0_weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='bulk_density_0_density_value',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='bulk_density_1_volume',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='bulk_density_1_empty_weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='bulk_density_1_weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='bulk_density_1_density_value',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='weak_rock_initial_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса начальная, гр'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='weak_rock_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса слабых зерен, гр'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='weak_rock_content',
            field=models.FloatField(blank=True, null=True, verbose_name='Содержание, %'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='average_density_dried_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса высушенной пробы, гр'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='average_density_weight_in_air',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса в насыщенном состоянии на воздухе, гр'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='average_density_weight_in_water',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса корзины и пробы в воде, гр'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='average_density_empty_basket_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса пустой корзины, гр'),
        ),
        migrations.AddField(
            model_name='crushed8267testresult',
            name='average_density_value',
            field=models.FloatField(blank=True, null=True, verbose_name='Средняя плотность'),
        ),
        
        # Обновляем verbose_name для существующих полей
        migrations.AlterField(
            model_name='crushed8267testresult',
            name='bulk_density_average',
            field=models.FloatField(blank=True, null=True, verbose_name='Средняя насыпная плотность'),
        ),
        migrations.AlterField(
            model_name='crushed8267testresult',
            name='clay_content',
            field=models.FloatField(blank=True, null=True, verbose_name='Содержание глины в комках, %'),
        ),
        migrations.AlterField(
            model_name='crushed8267testresult',
            name='clay_initial_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса начальная, гр'),
        ),
        migrations.AlterField(
            model_name='crushed8267testresult',
            name='clay_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса глины в комках, гр'),
        ),
        migrations.AlterField(
            model_name='crushed8267testresult',
            name='crushability_type',
            field=models.IntegerField(default=0, verbose_name='Вид породы'),
        ),
        migrations.AlterField(
            model_name='crushed8267testresult',
            name='dust_after_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса после промывки, гр'),
        ),
        migrations.AlterField(
            model_name='crushed8267testresult',
            name='dust_content',
            field=models.FloatField(blank=True, null=True, verbose_name='Содержание п/г, %'),
        ),
        migrations.AlterField(
            model_name='crushed8267testresult',
            name='dust_initial_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса начальная, гр'),
        ),
    ]
