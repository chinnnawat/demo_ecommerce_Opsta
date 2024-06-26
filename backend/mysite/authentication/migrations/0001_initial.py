# Generated by Django 5.0.6 on 2024-06-05 14:11

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerUserModel',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('userId', models.CharField(default=uuid.uuid4, editable=False, max_length=16, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=16, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='customer_users', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='customer_users', to='auth.permission')),
            ],
            options={
                'verbose_name': 'Customer User',
            },
        ),
    ]
