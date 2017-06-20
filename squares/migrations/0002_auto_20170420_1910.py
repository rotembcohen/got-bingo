# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-20 19:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('squares', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardCell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_val', models.PositiveSmallIntegerField()),
                ('y_val', models.PositiveSmallIntegerField()),
                ('marked', models.BooleanField(default=False)),
                ('wildcard', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='board',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='boardcell',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='squares.Board'),
        ),
        migrations.AddField(
            model_name='boardcell',
            name='square',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='squares.Square'),
        ),
    ]
