# Generated by Django 4.1.2 on 2022-11-01 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_neworder_in_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neworder',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]