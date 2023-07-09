# Generated by Django 4.2.3 on 2023-07-09 08:16

import account.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_user_is_phone_verified_remove_user_otp_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', account.manager.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_phone_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(default=1234, max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default=456789, max_length=12, unique=True),
            preserve_default=False,
        ),
    ]