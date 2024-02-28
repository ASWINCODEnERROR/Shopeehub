# Generated by Django 5.0.2 on 2024-02-27 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('admin', 'Admin'), ('superadmin', 'Superadmin')], default='user', max_length=10),
        ),
    ]