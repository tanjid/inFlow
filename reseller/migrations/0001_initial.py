# Generated by Django 4.1 on 2022-10-17 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reseller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('number', models.CharField(blank=True, max_length=15, null=True)),
                ('discount', models.IntegerField()),
                ('address', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResellerOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('sub_total', models.IntegerField(default=0)),
                ('additional_discount', models.IntegerField(default=0)),
                ('reseller_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reseller.reseller')),
            ],
        ),
        migrations.CreateModel(
            name='ResellerOrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Initial', 'Initial'), ('Shipping', 'Shipping'), ('Return', 'Return'), ('Complete', 'Complete')], default='Initial', max_length=10)),
                ('qty', models.IntegerField()),
                ('product_prices', models.IntegerField(blank=True, null=True)),
                ('item_totals', models.IntegerField(blank=True, null=True)),
                ('main_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reseller.resellerorder')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='products.product')),
            ],
        ),
    ]
