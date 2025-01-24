# Generated by Django 5.1.2 on 2025-01-24 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_remove_toolsinventorymovement_tool_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='base_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='is_best_seller',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='is_upcoming',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='order_count',
            field=models.IntegerField(default=0),
        ),
    ]
