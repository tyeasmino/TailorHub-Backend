# Generated by Django 5.1.2 on 2025-01-24 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_inventoryitem_base_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='fabric_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
