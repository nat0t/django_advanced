# Generated by Django 2.2.18 on 2021-04-15 06:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_auto_20210407_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 17, 6, 33, 9, 561742, tzinfo=utc)),
        ),
    ]
