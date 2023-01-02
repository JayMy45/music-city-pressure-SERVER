# Generated by Django 4.1.3 on 2023-01-02 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_details', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=1000)),
                ('request_date', models.DateField(blank=True, null=True)),
                ('date_completed', models.DateField(blank=True, null=True)),
                ('scheduled', models.BooleanField(default=False)),
                ('consultation', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('confirm', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
                ('address', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('date_hired', models.DateField(blank=True, null=True)),
                ('phone_number', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
                ('salary', models.FloatField()),
                ('specialty', models.CharField(max_length=155)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=155)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=155)),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=155)),
                ('class_name', models.CharField(max_length=155)),
                ('percent', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('label', models.CharField(blank=True, max_length=155, null=True)),
                ('image', models.CharField(max_length=400)),
                ('description', models.CharField(max_length=200)),
                ('details', models.CharField(max_length=300)),
                ('price', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceTypeEquipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tools', to='mcpressureapi.equipment')),
                ('service_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcpressureapi.servicetype')),
            ],
        ),
        migrations.AddField(
            model_name='servicetype',
            name='tools',
            field=models.ManyToManyField(blank=True, related_name='equipment_id', through='mcpressureapi.ServiceTypeEquipment', to='mcpressureapi.equipment'),
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcpressureapi.customer')),
                ('service_call', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcpressureapi.appointments')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeServiceTypeSpecialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tools', to='mcpressureapi.employee')),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcpressureapi.servicetype')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcpressureapi.specialty')),
            ],
        ),
        migrations.AddField(
            model_name='appointments',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='confirm', to='mcpressureapi.customer'),
        ),
        migrations.AddField(
            model_name='appointments',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mcpressureapi.employee'),
        ),
        migrations.AddField(
            model_name='appointments',
            name='progress',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mcpressureapi.progress'),
        ),
        migrations.AddField(
            model_name='appointments',
            name='service_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mcpressureapi.servicetype'),
        ),
    ]
