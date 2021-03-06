# Generated by Django 3.0.5 on 2020-05-12 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0075_auto_20200506_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='commune',
            name='population',
            field=models.PositiveIntegerField(blank=True, help_text="Nombre d'habitants estimé", null=True, verbose_name='Population'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='superficie',
            field=models.PositiveIntegerField(blank=True, help_text='Exprimée en hectares (ha)', null=True, verbose_name='Superficie'),
        ),
    ]
