# Generated by Django 5.0.4 on 2024-04-23 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_bug_assign_to_alter_bug_bug_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='impact',
            field=models.CharField(choices=[('Severe', 'Severe'), ('Normal', 'Normal')], default='severe', max_length=10),
        ),
    ]
