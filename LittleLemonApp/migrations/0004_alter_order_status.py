# Generated by Django 4.2.17 on 2024-12-14 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonApp', '0003_menuitem_available_menuitem_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], max_length=20),
        ),
    ]
