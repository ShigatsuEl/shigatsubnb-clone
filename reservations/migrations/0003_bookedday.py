# Generated by Django 3.1.7 on 2021-03-15 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_auto_20210223_1252'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookedDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('day', models.DateField()),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.reservation')),
            ],
            options={
                'verbose_name': 'Booked Day',
                'verbose_name_plural': 'Booked Days',
            },
        ),
    ]
