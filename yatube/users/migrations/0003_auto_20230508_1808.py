# Generated by Django 2.2.19 on 2023-05-08 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230508_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='/media/posts/user.png', null=True, upload_to='profile_pics'),
        ),
    ]