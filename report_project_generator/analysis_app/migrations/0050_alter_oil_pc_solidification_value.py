# Generated by Django 4.0.4 on 2023-04-08 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_app', '0049_oil_pc_corrosive_sulfur_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oil_pc',
            name='solidification_value',
            field=models.IntegerField(blank=True, null=True, verbose_name='Температура застывания'),
        ),
    ]
