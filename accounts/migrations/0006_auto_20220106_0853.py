# Generated by Django 3.2.9 on 2022-01-06 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20220105_1929'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=20)),
                ('street', models.CharField(max_length=20)),
                ('plaque', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.RemoveField(
            model_name='customeradress',
            name='city',
        ),
        migrations.RemoveField(
            model_name='customeradress',
            name='plaque',
        ),
        migrations.RemoveField(
            model_name='customeradress',
            name='street',
        ),
        migrations.AddField(
            model_name='customeradress',
            name='default',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='customeradress',
            name='customer',
        ),
        migrations.AddField(
            model_name='customeradress',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer', to='accounts.customer'),
        ),
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.ManyToManyField(related_name='address', through='accounts.CustomerAdress', to='accounts.Address'),
        ),
        migrations.AddField(
            model_name='customeradress',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_address', to='accounts.address'),
        ),
    ]