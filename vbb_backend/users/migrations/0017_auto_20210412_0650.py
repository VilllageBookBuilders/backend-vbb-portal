# Generated by Django 3.0.10 on 2021-04-12 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20210411_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programdirector',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.Headmaster'),
        ),
    ]
