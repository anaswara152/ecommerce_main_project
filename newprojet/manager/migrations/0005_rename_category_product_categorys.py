# Generated by Django 5.1.2 on 2024-10-23 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='categorys',
        ),
    ]
