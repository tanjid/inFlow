# Generated by Django 4.1.2 on 2022-11-02 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0021_employeepermission_dashboard_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeepermission',
            name='inven',
            field=models.BooleanField(default=False),
        ),
    ]