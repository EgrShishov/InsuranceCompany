# Generated by Django 5.0.4 on 2024-04-18 11:31

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyBranch',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='insurance_company_app.basemodel')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=16)),
            ],
            options={
                'verbose_name': 'Филиал',
                'verbose_name_plural': 'Филиалы',
            },
            bases=('insurance_company_app.basemodel',),
        ),
        migrations.CreateModel(
            name='InsuranceClient',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='insurance_company_app.basemodel')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=40)),
                ('second_name', models.CharField(max_length=40)),
                ('age', models.IntegerField()),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=16)),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
            bases=('insurance_company_app.basemodel',),
        ),
        migrations.CreateModel(
            name='InsuranceObject',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='insurance_company_app.basemodel')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Объект страхования',
                'verbose_name_plural': 'Объекты страхования',
            },
            bases=('insurance_company_app.basemodel',),
        ),
        migrations.CreateModel(
            name='InsuranceType',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='insurance_company_app.basemodel')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Вид страхования',
                'verbose_name_plural': 'Виды страхований',
            },
            bases=('insurance_company_app.basemodel',),
        ),
        migrations.CreateModel(
            name='InsuranceAgent',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='insurance_company_app.basemodel')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=40)),
                ('second_name', models.CharField(max_length=40)),
                ('age', models.IntegerField()),
                ('address', models.CharField(max_length=80)),
                ('phone_number', models.CharField(max_length=16)),
                ('branch_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance_company_app.companybranch')),
            ],
            options={
                'verbose_name': 'Страховой агент',
                'verbose_name_plural': 'Страховые агенты',
            },
            bases=('insurance_company_app.basemodel',),
        ),
        migrations.CreateModel(
            name='InsuranceContract',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='insurance_company_app.basemodel')),
                ('date', models.DateField()),
                ('insurance_sum', models.FloatField()),
                ('insurance_type', models.TextField()),
                ('tariff_rate', models.FloatField()),
                ('branch_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance_company_app.companybranch')),
            ],
            options={
                'verbose_name': 'Договор',
                'verbose_name_plural': 'Договора',
            },
            bases=('insurance_company_app.basemodel',),
        ),
    ]
