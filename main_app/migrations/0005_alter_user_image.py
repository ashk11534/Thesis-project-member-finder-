# Generated by Django 4.0.2 on 2022-02-12 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_user_name_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='images/avatar.png', upload_to=''),
        ),
    ]
