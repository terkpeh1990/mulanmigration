# Generated by Django 3.1.4 on 2022-03-30 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfers',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('transaction_date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Trcreatedby', to=settings.AUTH_USER_MODEL)),
                ('fromaccount_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='froms', to='accounts.sub_accounts')),
                ('modified_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trmodifiedby', to=settings.AUTH_USER_MODEL)),
                ('toaccount_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to', to='accounts.sub_accounts')),
            ],
        ),
    ]
