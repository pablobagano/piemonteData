# Generated by Django 4.2.7 on 2024-01-23 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("piemonteData", "0006_userprofile_root_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="root_id",
            field=models.IntegerField(null=True),
        ),
    ]
