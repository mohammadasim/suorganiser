# Generated by Django 3.0.5 on 2020-08-20 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('users', '0001_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=30, unique=True)),
                ('about', models.TextField()),
                ('name', models.CharField(max_length=255)),
                ('joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                (
                'user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
    ]
