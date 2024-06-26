# Generated by Django 5.0.2 on 2024-05-13 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_orderitem_sales_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('cash', 'Cash'), ('upi', 'UPI'), ('unsettled', 'Unsettled')], default='cash', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='executed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
