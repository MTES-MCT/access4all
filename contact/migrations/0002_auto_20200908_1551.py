# Generated by Django 3.0.7 on 2020-09-08 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sent_ok',
            field=models.BooleanField(default=False, verbose_name='Envoi OK'),
        ),
    ]
