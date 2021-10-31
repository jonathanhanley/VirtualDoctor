# Generated by Django 3.2.8 on 2021-10-27 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vdoc_api', '0006_auto_20211027_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=1028, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vdoc_api.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]