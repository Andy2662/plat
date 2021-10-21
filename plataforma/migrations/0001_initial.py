# Generated by Django 3.2.8 on 2021-10-20 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Csv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(upload_to='csvs')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('activated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='data_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitud', models.CharField(max_length=200, verbose_name='latitud')),
                ('longitud', models.CharField(max_length=200, verbose_name='longitud')),
                ('imsi', models.CharField(max_length=200, verbose_name='imsi')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='date')),
                ('test_name', models.CharField(max_length=200, verbose_name='test_name')),
                ('pot_db', models.CharField(max_length=200, verbose_name='pot_db')),
                ('operador', models.CharField(max_length=200, verbose_name='operador')),
                ('user', models.CharField(max_length=200, verbose_name='user')),
                ('observacion', models.CharField(max_length=200, verbose_name='observacion')),
            ],
        ),
    ]
