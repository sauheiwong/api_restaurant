# Generated by Django 4.2.1 on 2023-05-15 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_endpoint', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True, max_length=4192, null=True),
        ),
    ]
