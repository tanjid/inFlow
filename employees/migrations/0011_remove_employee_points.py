# Generated by Django 4.1.2 on 2022-10-31 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0010_delete_emplpyeepointshour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='points',
        ),
    ]