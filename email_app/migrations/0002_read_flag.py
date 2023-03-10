# Generated by Django 3.2.17 on 2023-02-24 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_app', '0001_email_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='email',
            name='sender_email',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
