# Generated by Django 2.2.5 on 2022-07-31 05:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20220721_0626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='purchase_timestamp',
            field=models.DateField(default=datetime.datetime(2022, 7, 31, 5, 5, 57, 10346)),
        ),
    ]
