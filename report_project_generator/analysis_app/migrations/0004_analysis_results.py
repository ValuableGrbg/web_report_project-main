# Generated by Django 4.0.4 on 2022-07-13 07:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analysis_app', '0003_alter_client_equipment_client_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='analysis_results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField(max_length=266, verbose_name='Заметки')),
                ('H2', models.FloatField(max_length=12, verbose_name='Водород')),
                ('CH4', models.FloatField(max_length=12, verbose_name='Метан')),
                ('C2H4', models.FloatField(max_length=12, verbose_name='Этилен')),
                ('C2H6', models.FloatField(max_length=12, verbose_name='Этан')),
                ('C2H2', models.FloatField(max_length=12, verbose_name='Ацетилен')),
                ('CO2', models.FloatField(max_length=12, verbose_name='Диоксид углерода')),
                ('CO', models.FloatField(max_length=12, verbose_name='Оксид углерода')),
                ('N2_O2', models.FloatField(max_length=12, verbose_name='ОГС')),
                ('SRG', models.FloatField(max_length=12, verbose_name='СРГ')),
                ('chromotograph', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='analysis_app.devices', verbose_name='Идентификатор диагностирующего хроматографа')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='analysis_app.client_equipment', verbose_name='Заказчик')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='Работник')),
            ],
            options={
                'verbose_name': 'Проведенные анализы',
                'verbose_name_plural': 'Проведенные анализы',
            },
        ),
    ]
