# Generated by Django 3.1.7 on 2021-04-11 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210324_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='is_head_teacher',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='HeadTeacher',
        ),
    ]
