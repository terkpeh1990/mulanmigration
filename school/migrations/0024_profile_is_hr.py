# Generated by Django 3.2.4 on 2021-09-15 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0023_pv_transaction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_hr',
            field=models.BooleanField(default=False),
        ),
    ]