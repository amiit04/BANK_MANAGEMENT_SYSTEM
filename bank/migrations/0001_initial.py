# Generated by Django 4.2.6 on 2023-10-30 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('account_number', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDetails',
            fields=[
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('father_name', models.CharField(max_length=100)),
                ('customer_id', models.CharField(max_length=7, unique=True)),
                ('account_number', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('mobile_number', models.CharField(max_length=10)),
                ('pin_code', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('account_number', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('mode', models.CharField(max_length=6)),
            ],
        ),
    ]