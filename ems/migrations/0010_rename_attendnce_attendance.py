# Generated by Django 4.1 on 2022-08-27 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0009_rename_attendenceemployee_attendanceemployee_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Attendnce',
            new_name='Attendance',
        ),
    ]