# Generated by Django 5.1.2 on 2025-01-07 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitMakers', '0004_alter_service_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitmaker',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
