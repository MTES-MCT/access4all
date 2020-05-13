# Generated by Django 3.0.5 on 2020-04-28 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0070_auto_20200428_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='erp',
            name='contact_email',
            field=models.EmailField(blank=True, help_text="Adresse email permettant de contacter l'ERP", max_length=255, null=True, verbose_name='Courriel'),
        ),
    ]