from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    watchlist = models.ManyToManyField('Listing', related_name='wishlists')

class Listing(models.Model):
    CATEGORY_CHOICES = (
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('books', 'Books'),
        ('home', 'Home'),
        ('toys', 'Toys'),
        ('sports', 'Sports'),
        ('food', 'Food'),
        ('art', 'Art'),
        ('jewelry', 'Jewelry'),
        ('automotive', 'Automotive'),
        ('real-estate', 'Real Estate'),
    )
    title = models.CharField(max_length=2000)
    description = models.TextField(max_length=1000, default="No description provided")
    image = models.URLField(max_length=200000, null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    current_bid = models.FloatField(default=0.0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)


class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    placed_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField(max_length=30000)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
