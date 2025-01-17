# Generated by Django 5.1.2 on 2025-01-17 15:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitMakers', '0008_remove_service_icon'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('fabric_type', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=10)),
                ('image_url', models.URLField(blank=True, max_length=255, null=True)),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('is_on_sale', models.BooleanField(default=False)),
                ('stock_quantity', models.IntegerField(default=0)),
                ('min_stock_level', models.IntegerField(default=5)),
                ('is_available', models.BooleanField(default=True)),
                ('supplier_name', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order_count', models.IntegerField(default=0)),
                ('total_sales', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('is_best_seller', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitMakers.category')),
                ('fit_maker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitMakers.fitmaker')),
            ],
        ),
        migrations.CreateModel(
            name='DressRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], decimal_places=1, default=0, max_digits=2)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='fitMakers.dress')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('dress', 'user')},
            },
        ),
    ]
