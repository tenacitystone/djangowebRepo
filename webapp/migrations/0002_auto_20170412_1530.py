# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-12 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=8)),
                ('user_password', models.CharField(max_length=100)),
                ('user_phone_number', models.IntegerField()),
                ('user_address', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='production',
            name='pPrice',
            field=models.FloatField(default=1, max_length=5),
            preserve_default=False,
        ),
    ]
