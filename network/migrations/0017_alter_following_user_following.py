# Generated by Django 3.2.9 on 2021-12-11 22:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0016_alter_following_user_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='following',
            name='user_following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
