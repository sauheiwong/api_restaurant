# Generated by Django 4.2.1 on 2023-05-14 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_endpoint', '0007_order_created_at_order_updated_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderfood',
            name='price',
        ),
    ]
