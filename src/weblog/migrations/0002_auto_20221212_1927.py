# Generated by Django 3.2 on 2022-12-12 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='picture',
            new_name='picture_1',
        ),
        migrations.AddField(
            model_name='post',
            name='picture_2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='post',
            name='picture_3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='post',
            name='picture_4',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='post',
            name='picture_5',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
