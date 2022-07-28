# Generated by Django 3.1.4 on 2022-04-29 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_transfers_tran_dec'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfers',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Comfirmed', 'Comfirmed'), ('Cancelled', 'Cancelled')], default='Comfirmed', max_length=10),
        ),
    ]
