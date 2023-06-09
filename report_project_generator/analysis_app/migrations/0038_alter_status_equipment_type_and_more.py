# Generated by Django 4.0.4 on 2022-10-18 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_app', '0037_alter_status_equipment_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='equipment_type',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='analysis_app.equipmentandtestingpart'),
        ),
        migrations.AlterField(
            model_name='status',
            name='test_type_and_doc',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='analysis_app.oiltesttypesinfo'),
        ),
    ]
