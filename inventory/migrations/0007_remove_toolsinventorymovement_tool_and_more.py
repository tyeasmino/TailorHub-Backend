# Generated by Django 5.1.2 on 2025-01-10 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_inventoryitem_sell_price_per_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toolsinventorymovement',
            name='tool',
        ),
        migrations.DeleteModel(
            name='ToolsInventory',
        ),
        migrations.DeleteModel(
            name='ToolsInventoryMovement',
        ),
    ]
