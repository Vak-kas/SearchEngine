# Generated by Django 5.1.1 on 2024-10-14 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urls',
            name='write_at',
            field=models.CharField(max_length=255),
        ),
    ]
