# Generated by Django 3.0.4 on 2020-04-25 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
            ],
        ),
    ]
