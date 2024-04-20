# Generated by Django 5.0.4 on 2024-04-20 18:27

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_company_app', '0007_basemodel_created_at_withtz_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 20, 18, 27, 6, 106047, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='basemodel',
            name='created_at_withTZ',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 20, 18, 27, 6, 106047, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='insurancecontract',
            name='insurance_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance_company_app.insurancetype'),
        ),
    ]