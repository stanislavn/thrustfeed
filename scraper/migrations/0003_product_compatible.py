# Generated by Django 3.1.5 on 2021-01-22 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_auto_20210121_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='compatible',
            field=models.CharField(blank=True, max_length=2200, null=True),
        ),
    ]
