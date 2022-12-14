# Generated by Django 3.1.4 on 2022-06-20 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0023_auto_20220609_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bclosing_stock_summery',
            name='close_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='bopening_stock_summery',
            name='close_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order_details',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bakery.order'),
        ),
        migrations.AlterField(
            model_name='order_details',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bakery.product'),
        ),
    ]
