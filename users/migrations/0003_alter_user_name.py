# Generated by Django 4.0.4 on 2022-05-11 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_remove_user_username_alter_user_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=255),
        ),
    ]