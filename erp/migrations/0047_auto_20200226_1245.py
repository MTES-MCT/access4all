# Generated by Django 3.0.3 on 2020-02-26 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0046_auto_20200226_1234'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cheminement',
            unique_together={('accessibilite', 'type', 'nom')},
        ),
    ]