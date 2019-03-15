# Generated by Django 2.0.13 on 2019-03-15 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.CharField(max_length=10, verbose_name='date published')),
                ('rate', models.CharField(max_length=10)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='currencies.Currency')),
            ],
        ),
    ]
