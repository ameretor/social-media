# Generated by Django 3.2.9 on 2021-12-10 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_alter_userprofile_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='following',
            options={'verbose_name': 'Following', 'verbose_name_plural': 'Followings'},
        ),
        migrations.AlterModelOptions(
            name='posts',
            options={'verbose_name': 'post', 'verbose_name_plural': 'posts'},
        ),
        migrations.AlterUniqueTogether(
            name='following',
            unique_together={('user', 'user_follower', 'post')},
        ),
    ]