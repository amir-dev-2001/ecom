# Generated by Django 3.2 on 2022-12-12 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20221209_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='postal_code',
            field=models.TextField(blank=True, max_length=10, null=True),
        ),
    ]
