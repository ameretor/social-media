# Generated by Django 3.2.9 on 2021-12-09 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_alter_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='images/default.png', null=True, upload_to='images/'),
        ),
    ]