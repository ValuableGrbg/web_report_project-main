# Generated by Django 4.0.4 on 2022-10-13 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_app', '0022_oilprobesissues_alter_oiltesttypesinfo_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis_results',
            name='probe_code',
            field=models.CharField(default=None, max_length=30, verbose_name='Шифр пробы'),
        ),
    ]
