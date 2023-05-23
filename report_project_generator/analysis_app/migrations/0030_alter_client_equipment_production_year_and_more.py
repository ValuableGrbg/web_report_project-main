# Generated by Django 4.0.4 on 2022-10-14 16:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_app', '0029_client_equipment_production_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client_equipment',
            name='production_year',
            field=models.PositiveIntegerField(default=None, help_text='Год в формате: YYYY', null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2022)], verbose_name='Год изготовления'),
        ),
        migrations.AlterField(
            model_name='client_equipment',
            name='setting_year',
            field=models.PositiveIntegerField(default=None, help_text='Год в формате: YYYY', null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2022)], verbose_name='Год установки'),
        ),
    ]
