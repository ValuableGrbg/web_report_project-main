# Generated by Django 4.0.4 on 2022-10-18 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_app', '0038_alter_status_equipment_type_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TransformersLimitValues_35_220_STO',
            new_name='ChargTransformersLimitValues_35_220_STO',
        ),
    ]
