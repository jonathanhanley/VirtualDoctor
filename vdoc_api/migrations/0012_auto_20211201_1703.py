# Generated by Django 3.2.8 on 2021-12-01 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vdoc_api', '0011_auto_20211117_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_consultant',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='parent_q',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vdoc_api.question'),
        ),
    ]
