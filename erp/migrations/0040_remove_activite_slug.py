# Generated by Django 3.0.3 on 2020-02-12 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0039_auto_20200212_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activite',
            name='slug',
        ),
    ]
