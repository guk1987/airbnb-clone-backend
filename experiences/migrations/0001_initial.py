# Generated by Django 5.0 on 2023-12-10 08:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('detail', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.TextField(blank=True, max_length=150, null=True)),
            ],
            options={
                'verbose_name_plural': 'Perks',
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='', max_length=140)),
                ('country', models.CharField(default='대한민국', max_length=50)),
                ('city', models.CharField(default='서울', max_length=80)),
                ('price', models.PositiveIntegerField()),
                ('address', models.CharField(max_length=250)),
                ('start_at', models.TimeField()),
                ('end_at', models.TimeField()),
                ('description', models.TextField()),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('perks', models.ManyToManyField(to='experiences.perk')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
