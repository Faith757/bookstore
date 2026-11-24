from django.db import models
from django.conf import settings
from books.models import Book

# Create your models here.
class Cart(models.Model):
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete = models.CASCADE
    )
    
    book = models.ForeignKey(Book, on_delete = models.PROTECT)
    quantity = models.IntegerField(default = 1)
    stock_reserved = models.BooleanField(default = False)
    date_added = models.DateField(auto_now_add = True)

    @property
    def subtotal(self):
        return self.book.price * self.quantity