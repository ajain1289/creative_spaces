# Generated by Django 3.0.4 on 2020-05-01 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoleDetail',
            fields=[
                ('name', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('email', models.EmailField(blank=True, default='', max_length=255, primary_key=True, serialize=False)),
                ('password', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('mobile', models.BigIntegerField(blank=True, default=0, null=True)),
                ('gender', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('address', models.TextField(blank=True, default='', max_length=255, null=True)),
                ('verify_link', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('otp', models.IntegerField(blank=True, default=0, null=True)),
                ('otp_time', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('is_active', models.NullBooleanField(default=False)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='backend_app.UserRole')),
            ],
        ),
    ]
