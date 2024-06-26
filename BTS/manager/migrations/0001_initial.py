# Generated by Django 5.0.4 on 2024-04-22 12:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('bug_count', models.IntegerField(default=0)),
            ],
        ),
    ]
