# Generated by Django 5.0.4 on 2024-04-20 12:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_company_app', '0005_insuranceagent_user_alter_basemodel_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 20, 12, 57, 43, 986364, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='insuranceagent',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]