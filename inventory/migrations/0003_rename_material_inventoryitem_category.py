# Generated by Django 5.1.2 on 2025-01-06 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_inventoryitem_inventoryitemmovement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventoryitem',
            old_name='material',
            new_name='category',
        ),
    ]
