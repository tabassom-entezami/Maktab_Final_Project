# Generated by Django 3.2.9 on 2022-01-03 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customer_device'),
        ('resturant', '0013_auto_20220103_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_id',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.customer'),
            preserve_default=False,
        ),
    ]
