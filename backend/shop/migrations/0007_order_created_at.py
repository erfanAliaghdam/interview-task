# Generated by Django 4.1.6 on 2024-01-04 23:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0006_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
