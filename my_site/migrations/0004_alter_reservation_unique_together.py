# Generated by Django 5.0.4 on 2025-01-14 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0003_delete_post'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('table_number', 'reservation_time')},
        ),
    ]
