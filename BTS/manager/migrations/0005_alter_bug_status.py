# Generated by Django 5.0.4 on 2024-04-23 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_alter_bug_impact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='status',
            field=models.CharField(choices=[('Open', 'True'), ('Closed', 'Closed')], default='Open', max_length=10),
        ),
    ]
