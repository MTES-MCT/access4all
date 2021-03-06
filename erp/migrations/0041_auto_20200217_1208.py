# Generated by Django 3.0.3 on 2020-02-17 11:08

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0040_remove_activite_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='erp',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(null=True, verbose_name='Search vector'),
        ),
        migrations.AddIndex(
            model_name='erp',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='erp_erp_search__717de3_gin'),
        ),
    ]
