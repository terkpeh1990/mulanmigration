# Generated by Django 3.2.4 on 2021-11-10 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0017_auto_20211110_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snack_detail',
            name='snack',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bakery.snacks'),
        ),
    ]