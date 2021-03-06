# Generated by Django 4.0.4 on 2022-05-10 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contract_app', '0006_rename_inspection_general_inspectiongeneral_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwoTypeService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено в')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contract_app.typeservice', verbose_name='Xizmat turi')),
            ],
        ),
    ]
