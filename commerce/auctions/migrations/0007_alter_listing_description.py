# Generated by Django 4.2.4 on 2023-08-24 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(default='No description provided', max_length=3000),
        ),
    ]
