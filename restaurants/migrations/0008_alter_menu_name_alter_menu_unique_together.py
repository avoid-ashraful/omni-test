# Generated by Django 4.0.4 on 2022-05-10 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0007_alter_menu_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together={('restaurant', 'name')},
        ),
    ]
