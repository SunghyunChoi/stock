# Generated by Django 3.1.4 on 2021-01-07 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='Article',
            new_name='article',
        ),
    ]
