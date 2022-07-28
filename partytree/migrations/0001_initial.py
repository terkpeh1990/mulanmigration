# Generated by Django 3.1.4 on 2021-06-01 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.CharField(max_length=2000, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Daily_Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_date', models.DateField()),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.CharField(max_length=2000, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('images', models.ImageField(blank=True, null=True, upload_to='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partytree.categorys')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.CharField(max_length=2000, primary_key=True, serialize=False)),
                ('order_date', models.DateField(blank=True, null=True)),
                ('gross_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('vat', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('payments', models.CharField(blank=True, choices=[('Part Payment', 'Part Payment'), ('Full Payment', 'Full Paument'), ('No Payment', 'No Payment')], max_length=25, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('money_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('money_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='partytree.customers')),
                ('daily_session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='partytree.daily_session')),
            ],
        ),
        migrations.CreateModel(
            name='Order_Detailss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('gross_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='partytree.orders')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='partytree.products')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.CharField(max_length=2000, primary_key=True, serialize=False)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='partytree.orders')),
            ],
        ),
        migrations.CreateModel(
            name='Inventorys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instock', models.PositiveIntegerField(default=0)),
                ('outgoing', models.PositiveIntegerField(default=0)),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('avialable_stock', models.PositiveIntegerField(default=0)),
                ('avialable_stock_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partytree.products')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory_recordss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('avialable_stock_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('status', models.CharField(blank=True, choices=[('Incoming', 'Incoming'), ('Outgoing', 'Outgoing')], max_length=10, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partytree.products')),
            ],
        ),
        migrations.CreateModel(
            name='Damagess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('damage_date', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partytree.products')),
            ],
        ),
        migrations.CreateModel(
            name='Closing_stockss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('closing_stock', models.PositiveIntegerField(default=0)),
                ('avialable_stock_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('closing_stock_date', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partytree.products')),
            ],
        ),
    ]
