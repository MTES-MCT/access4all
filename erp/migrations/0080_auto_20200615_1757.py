# Generated by Django 3.0.7 on 2020-06-15 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('erp', '0079_auto_20200527_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='erp',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Administration'), ('gestionnaire', 'Gestionnaire'), ('public', 'Utilisateur public'), ('system', 'Système')], default='system', max_length=50, verbose_name='Profil de contributeur'),
        ),
        migrations.AlterField(
            model_name='erp',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Contributeur'),
        ),
        migrations.AddIndex(
            model_name='erp',
            index=models.Index(fields=['user_type'], name='erp_erp_user_ty_1813ad_idx'),
        ),
    ]