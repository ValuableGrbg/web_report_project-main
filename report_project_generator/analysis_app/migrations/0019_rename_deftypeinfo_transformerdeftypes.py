# Generated by Django 4.0.4 on 2022-10-09 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_app', '0018_delete_transformerdeftypes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DefTypeInfo',
            new_name='TransformerDefTypes',
        ),
    ]
