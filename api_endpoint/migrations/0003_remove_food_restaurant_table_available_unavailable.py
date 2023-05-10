# Generated by Django 4.2.1 on 2023-05-10 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_endpoint', '0002_food_type_alter_table_restaurant_orderfood_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='restaurant',
        ),
        migrations.AddField(
            model_name='table',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Unavailable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unavailable_food', to='api_endpoint.food')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unavailable_restaurant', to='api_endpoint.restaurant')),
            ],
        ),
    ]
