# Generated by Django 3.2.8 on 2021-11-10 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vdoc_api', '0008_satisfy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loop_amount', models.IntegerField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vdoc_api.question')),
            ],
        ),
    ]
