# Generated by Django 5.1.2 on 2024-10-30 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_ordertb_orderitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertb',
            name='paymentdate',
            field=models.CharField(max_length=18),
        ),
        migrations.AlterField(
            model_name='ordertb',
            name='shippingdate',
            field=models.CharField(max_length=18),
        ),
    ]
