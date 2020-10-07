# Generated by Django 3.1.1 on 2020-10-06 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AWSRole',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('name', models.CharField(max_length=100, unique=True)),
                ('policy', models.CharField(choices=[], max_length=100)),
                ('trust', models.TextField(blank=True)),
                ('user', models.BooleanField(default=False)),
                ('mfa', models.BooleanField(default=False)),
                ('kms', models.BooleanField(default=False)),
                ('ec2', models.BooleanField(default=False)),
                ('aws_lambda', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('name', 'user')},
            },
        ),
        migrations.CreateModel(
            name='AccessRole',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('access_key', models.CharField(
                    blank=True, max_length=100, null=True
                )),
                ('secret_key', models.CharField(
                    blank=True, max_length=100, null=True
                )),
                ('group', models.ForeignKey(
                    blank=True, null=True, to='auth.group',
                    on_delete=django.db.models.deletion.CASCADE
                )),
                ('role', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='akeru.awsrole'
                )),
                ('user', models.ForeignKey(
                    blank=True, null=True, to=settings.AUTH_USER_MODEL,
                    on_delete=django.db.models.deletion.CASCADE
                )),
            ],
        ),
    ]
