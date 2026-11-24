from django.db import models

# Create your models here.
class Book(models.Model):
    category_choice = [
        ('fiction', 'fiction'),
        ('science', 'science'),
        ('technology', 'technology'),
        ('education', 'education'),
        ('business', 'business'),
        ('history', 'history')
    ]
    title = models.CharField()
    author = models.CharField()
    isbn = models.CharField(unique = True)
    category = models.CharField( choices = category_choice)
    publisher = models.CharField()
    year = models.CharField()
    price = models.IntegerField()
    quantity = models.IntegerField(default = 0)
    date_added = models.DateTimeField(auto_now_add = True)
    date_updated = models.DateTimeField(auto_now_add = True)

    @property
    def is_available(self):
        return self.quantity > 0
