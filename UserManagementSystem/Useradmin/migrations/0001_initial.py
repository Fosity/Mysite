# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-30 08:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='用户组名')),
            ],
        ),
        migrations.CreateModel(
            name='User2Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Useradmin.Group', verbose_name='用户组')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
            ],
        ),
        migrations.AddField(
            model_name='user2group',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Useradmin.UserInfo', verbose_name='用户'),
        ),
    ]