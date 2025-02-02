# Generated by Django 5.0.4 on 2025-01-14 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_registered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
