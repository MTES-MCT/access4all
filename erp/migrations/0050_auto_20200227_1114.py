# Generated by Django 3.0.3 on 2020-02-27 10:14

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0049_auto_20200226_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activite',
            name='mots_cles',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=40), blank=True, default=list, help_text='Liste de mots-clés apparentés à cette activité', null=True, size=None, verbose_name='Mots-clés'),
        ),
    ]