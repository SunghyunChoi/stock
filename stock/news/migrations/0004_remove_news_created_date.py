# Generated by Django 3.1.4 on 2021-01-03 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20210103_2148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='created_date',
        ),
    ]
