# Generated by Django 2.2.3 on 2019-08-22 12:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customuser_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='created',
        ),
        migrations.AddField(
            model_name='customuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
