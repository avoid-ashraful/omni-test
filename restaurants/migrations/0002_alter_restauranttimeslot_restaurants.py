# Generated by Django 4.0.4 on 2022-05-10 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="restauranttimeslot",
            name="restaurants",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="time_slots",
                to="restaurants.restaurant",
            ),
        ),
    ]
