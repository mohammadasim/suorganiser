# Generated by Django 3.0.5 on 2020-08-21 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0007_auto_20200428_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsLinkManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StartupManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
