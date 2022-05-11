# Generated by Django 4.0.4 on 2022-05-10 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0003_rename_restaurants_restauranttimeslot_restaurant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="restauranttimeslot",
            name="day",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "Mon"),
                    (2, "Tues"),
                    (3, "Weds"),
                    (4, "Thurs"),
                    (5, "Fri"),
                    (6, "Sat"),
                    (7, "Sun"),
                ]
            ),
        ),
    ]