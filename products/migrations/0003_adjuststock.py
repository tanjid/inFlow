# Generated by Django 4.1 on 2022-10-18 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdjustStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('cause', models.CharField(max_length=20)),
                ('note', models.TextField(blank=True, null=True)),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='products.product')),
            ],
        ),
    ]
