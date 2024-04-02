# Generated by Django 5.0.2 on 2024-03-29 11:03

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('barcode', models.CharField(blank=True, max_length=50)),
                ('sales_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField(default=0)),
                ('warning_limit', models.IntegerField(default=0)),
                ('unit', models.CharField(max_length=20)),
                ('featured', models.BooleanField(default=False)),
                ('unlimited', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, upload_to='product_images/')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.business')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('variant_id', models.CharField(max_length=20, unique=True)),
                ('barcode', models.CharField(blank=True, max_length=50)),
                ('sales_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField(default=0)),
                ('warning_limit', models.IntegerField(default=0)),
                ('unit', models.CharField(max_length=20)),
                ('unlimited', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, upload_to='variant_images/')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='product.product')),
            ],
        ),
    ]
