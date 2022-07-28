# Generated by Django 3.1.4 on 2022-03-20 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partytree', '0003_auto_20220118_0723'),
    ]

    operations = [
        migrations.AddField(
            model_name='damagess',
            name='cause',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='damagess',
            name='clear',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='damagess',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='damagess',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='damagess',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dcreatedbys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='damagess',
            name='dastatus',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='damagess',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='damagess',
            name='modified_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dmodifiedbys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='HistoricalDamagess',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('damage_date', models.DateTimeField(blank=True, editable=False)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('cause', models.CharField(max_length=255)),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('dastatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled')], max_length=10, null=True)),
                ('clear', models.BooleanField(default=False)),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('modified', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('product_id', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='partytree.products')),
            ],
            options={
                'verbose_name': 'historical damagess',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
