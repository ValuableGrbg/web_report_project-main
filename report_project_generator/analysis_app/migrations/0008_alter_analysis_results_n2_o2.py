# Generated by Django 4.0.4 on 2022-07-14 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_app', '0007_rename_date_analysis_results_analysis_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis_results',
            name='N2_O2',
            field=models.FloatField(blank=True, default=None, max_length=12, null=True, verbose_name='ОГС'),
        ),
    ]
