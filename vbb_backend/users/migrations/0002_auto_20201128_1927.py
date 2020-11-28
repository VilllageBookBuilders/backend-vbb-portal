# Generated by Django 3.0.10 on 2020-11-28 19:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='external_id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]