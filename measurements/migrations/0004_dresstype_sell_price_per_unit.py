# Generated by Django 5.1.2 on 2025-01-08 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0003_alter_dressmeasurement_fit_finder'),
    ]

    operations = [
        migrations.AddField(
            model_name='dresstype',
            name='sell_price_per_unit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
