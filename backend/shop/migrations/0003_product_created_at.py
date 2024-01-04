# Generated by Django 4.1.6 on 2024-01-04 13:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0002_product_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
