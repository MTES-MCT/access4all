# Generated by Django 3.0.5 on 2020-05-06 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0074_auto_20200505_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='erp',
            name='commune_ext',
            field=models.ForeignKey(blank=True, help_text='La commune de cet établissement', null=True, on_delete=django.db.models.deletion.SET_NULL, to='erp.Commune', verbose_name='Commune (relation)'),
        ),
    ]
