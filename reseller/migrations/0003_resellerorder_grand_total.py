# Generated by Django 4.1 on 2022-10-17 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reseller', '0002_alter_resellerorder_additional_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='resellerorder',
            name='grand_total',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
