# Generated by Django 4.2.4 on 2023-08-29 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_alter_comment_comment_alter_listing_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wishlist',
            field=models.ManyToManyField(related_name='wishlists', to='auctions.listing'),
        ),
    ]
