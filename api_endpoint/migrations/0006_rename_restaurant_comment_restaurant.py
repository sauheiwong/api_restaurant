# Generated by Django 4.2.1 on 2023-05-16 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_endpoint', '0005_food_no_of_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='Restaurant',
            new_name='restaurant',
        ),
    ]
