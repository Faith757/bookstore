from django.db import models
from django.conf import settings
from books.models import Book
from carts.models import Cart

# Create your models here.
class Order(models.Model):
    Status_choice = [
        ('', 'select status'),
        ('pending', 'pending'),
        ('processing', 'processing'),
        ('shipped', 'shipped'),
        ('delivered', 'delivered'),
        ('cancelled', 'cancelled'),
    ]
    payment_choice = [
        ('', 'select payment'),
        ('pending', 'pending'),
        ('paid', 'paid'),
        ('reversed', 'reversed')
    ]

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.PROTECT,
        related_name = 'orders'
    )
    payment_reference = models.CharField(unique = True, blank = True, null = True)
    payment_receipt = models.ImageField(upload_to = 'payment_receipts/', blank = True, null = True)
    total_amount = models.IntegerField()
    date_ordered = models.DateTimeField(auto_now_add = True)
    status = models.CharField( choices = Status_choice, default = "pending")
    payment = models.CharField(choices = payment_choice, default = 'pending')
    cart_cleared = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.payment == 'paid' and not self.cart_cleared:
            Cart.objects.filter(member = self.member).delete()
            Order.objects.filter(pk = self.pk).update(cart_cleared = True)
            self.cart_cleared = True

class orderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete = models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete = models.SET_NULL,
        null = True,
        blank = True
    )

    cart = models.ForeignKey(Cart, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'ordered_items')
    book_title = models.CharField()
    price = models.IntegerField()
    quantity = models.IntegerField()

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return self.book_title