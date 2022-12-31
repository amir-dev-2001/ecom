# Generated by Django 3.2 on 2022-12-09 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product_id',
        ),
        migrations.AddField(
            model_name='order',
            name='product_id',
            field=models.ManyToManyField(to='api.Product'),
        ),
    ]
