# Generated by Django 5.0.4 on 2024-05-05 17:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_company_app', '0013_insurancecontract_insurance_object_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='insuranceagent',
            name='photo',
            field=models.ImageField(default='C:\\django\\insurance_company\\media\\images\news\natamog.jpg', upload_to='images/agents_photos'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='basemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 17, 11, 48, 524353, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='basemodel',
            name='created_at_withTZ',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 17, 11, 48, 524353, tzinfo=datetime.timezone.utc)),
        ),
    ]
