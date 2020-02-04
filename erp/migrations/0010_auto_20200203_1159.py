# Generated by Django 3.0.2 on 2020-02-03 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0009_auto_20200203_1130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='erp',
            name='accessibilite',
        ),
        migrations.AddField(
            model_name='accessibilite',
            name='erp',
            field=models.OneToOneField(blank=True, help_text='ERP', null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.Erp'),
        ),
    ]
