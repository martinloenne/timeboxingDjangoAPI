# Generated by Django 2.2.3 on 2019-08-22 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190819_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='created',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
