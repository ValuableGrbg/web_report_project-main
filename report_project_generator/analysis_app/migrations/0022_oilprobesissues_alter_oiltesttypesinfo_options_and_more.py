# Generated by Django 4.0.4 on 2022-10-13 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_app', '0021_alter_client_equipment_equipment_type_full_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OilProbesIssues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('probe_issue_type', models.CharField(max_length=20, verbose_name='Название причины испытания масла')),
            ],
            options={
                'verbose_name': 'причину проведения испытаний',
                'verbose_name_plural': 'причины проведения испытаний',
            },
        ),
        migrations.AlterModelOptions(
            name='oiltesttypesinfo',
            options={'verbose_name': 'информацию о типах проводимых испытаний', 'verbose_name_plural': 'информация о типах проводимых испытаний'},
        ),
        migrations.AlterModelOptions(
            name='probedetailsinfo',
            options={'verbose_name': 'информацию об отборе', 'verbose_name_plural': 'Информация об отборе'},
        ),
        migrations.AddField(
            model_name='probedetailsinfo',
            name='test_doc_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, to='analysis_app.oiltesttypesinfo', verbose_name='Вид испытания'),
        ),
        migrations.AlterField(
            model_name='oiltesttypesinfo',
            name='normative_doc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='analysis_app.oilnormativedocs', verbose_name='Нормативный документ'),
        ),
        migrations.AlterField(
            model_name='probedetailsinfo',
            name='probe_issue',
            field=models.CharField(default=None, max_length=100, verbose_name='Причина отбора'),
        ),
    ]
