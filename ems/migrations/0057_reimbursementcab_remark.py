# Generated by Django 4.1 on 2022-10-04 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0056_reimbursementcab'),
    ]

    operations = [
        migrations.AddField(
            model_name='reimbursementcab',
            name='remark',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]