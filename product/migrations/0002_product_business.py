# Generated by Django 5.0.2 on 2024-03-11 10:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_expense_business'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='business',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='core.business'),
            preserve_default=False,
        ),
    ]