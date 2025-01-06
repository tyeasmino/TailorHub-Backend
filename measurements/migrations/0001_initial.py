# Generated by Django 5.1.2 on 2025-01-06 19:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DressType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=60)),
                ('icon', models.CharField(blank=True, max_length=20, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DressMeasurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dress_long', models.IntegerField()),
                ('chest_or_hip', models.IntegerField()),
                ('hand_pocket_length', models.IntegerField(blank=True, null=True)),
                ('hand_pant_start', models.IntegerField(blank=True, null=True)),
                ('hand_pant_end', models.IntegerField(blank=True, null=True)),
                ('neckband', models.IntegerField(blank=True, null=True)),
                ('dress_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='measurements.dresstype')),
            ],
        ),
    ]
