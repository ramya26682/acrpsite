# Generated by Django 2.1.1 on 2020-10-16 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20201016_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='Expected_Graduation',
            field=models.DateField(blank=True, max_length=20, null=True),
        ),
    ]
