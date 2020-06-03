# Generated by Django 3.0.6 on 2020-05-27 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0078_delete_equipementmalentendant'),
    ]

    operations = [
        migrations.AddField(
            model_name='erp',
            name='source',
            field=models.CharField(default='access4all', help_text='Nom de la source de données dont est issu cet ERP', max_length=100, null=True, verbose_name='Source'),
        ),
        migrations.AddField(
            model_name='erp',
            name='source_id',
            field=models.CharField(help_text="Identifiant de l'ERP dans la source initiale de données", max_length=255, null=True, verbose_name='Source ID'),
        ),
        migrations.AddIndex(
            model_name='erp',
            index=models.Index(fields=['source', 'source_id'], name='erp_erp_source_ca3d57_idx'),
        ),
    ]