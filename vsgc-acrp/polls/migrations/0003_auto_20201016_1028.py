# Generated by Django 2.1.1 on 2020-10-16 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20201016_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='visa_expiration',
            field=models.DateField(blank=True, max_length=10, null=True),
        ),
    ]
