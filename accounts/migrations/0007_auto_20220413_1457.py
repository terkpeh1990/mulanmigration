# Generated by Django 3.1.4 on 2022-04-13 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0006_auto_20220413_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsub_accounts',
            name='tag',
            field=models.CharField(choices=[('Mulan', 'Mulan'), ('Partytree', 'Partytree')], default='Mulan', max_length=20),
        ),
        migrations.AddField(
            model_name='sub_accounts',
            name='tag',
            field=models.CharField(choices=[('Mulan', 'Mulan'), ('Partytree', 'Partytree')], default='Mulan', max_length=20),
        ),
        migrations.AlterField(
            model_name='pv_payment_history',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hiscreatedby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pv_payment_history',
            name='modified_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hismodifiedby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transfers',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Trcreatedby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transfers',
            name='modified_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trmodifiedby', to=settings.AUTH_USER_MODEL),
        ),
    ]