# Generated by Django 4.0.4 on 2023-04-23 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_app', '0052_pc_limitvalues_color_limit_value_ons_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pc_limitvalues',
            name='color_limit_value_ons',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='pc_limitvalues',
            name='color_limit_value_pd',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='pc_limitvalues',
            name='transparency_limit_value_ons',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Прозрачность'),
        ),
        migrations.AlterField(
            model_name='pc_limitvalues',
            name='transparency_limit_value_pd',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Прозрачность'),
        ),
    ]