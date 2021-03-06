# Generated by Django 3.0.3 on 2020-02-12 15:41

from django.db import migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ("erp", "0038_activite_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activite",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                default="generic",
                editable=False,
                null=True,
                populate_from="nom",
            ),
        ),
    ]
