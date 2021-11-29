# Generated by Django 3.2.8 on 2021-11-17 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vdoc_api', '0009_loop'),
    ]

    operations = [
        migrations.AddField(
            model_name='loop',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='sub_should_loop',
            field=models.BooleanField(default=False),
        ),
    ]