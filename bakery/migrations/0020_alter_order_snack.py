# Generated by Django 3.2.4 on 2021-11-10 02:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0019_alter_order_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='snack',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bakery.snacks'),
        ),
    ]
