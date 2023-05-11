# Generated by Django 4.2 on 2023-05-04 07:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("listing", models.CharField(max_length=200)),
                ("listing_id", models.IntegerField()),
                ("name", models.CharField(max_length=200)),
                ("email", models.CharField(max_length=200)),
                ("phone", models.CharField(max_length=200)),
                ("message", models.CharField(blank=True)),
                (
                    "contact_date",
                    models.DateField(blank=True, default=datetime.datetime.now),
                ),
                ("user_id", models.IntegerField(blank=True)),
            ],
        ),
    ]