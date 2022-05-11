# Generated by Django 4.0.4 on 2022-05-10 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract_app', '0005_alter_oferta_adress_location'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='inspection_general',
            new_name='InspectionGeneral',
        ),
        migrations.RenameModel(
            old_name='Oferta_detail',
            new_name='OfertaDetail',
        ),
        migrations.RenameModel(
            old_name='type_service',
            new_name='TypeService',
        ),
        migrations.AlterField(
            model_name='oferta',
            name='product_type',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.DeleteModel(
            name='product_type',
        ),
    ]
