# Generated by Django 3.0.10 on 2020-12-10 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0003_auto_20201128_2037'),
    ]

    operations = [
        migrations.RenameField(
            model_name='computer',
            old_name='mentor_program',
            new_name='program',
        ),
    ]