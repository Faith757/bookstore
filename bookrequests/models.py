from django.db import models
from django.conf import settings
from books.models import Book

# Create your models here.
class bookRequest(models.Model):
    status_choice = [
        ('', 'select choice'),
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('rejected', 'rejected')
    ]
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )

    status = models.CharField(
        choices = status_choice,
        default = 'pending'
    )
    
    title = models.CharField()
    category = models.CharField()
    date_requested = models.DateTimeField(auto_now_add = True)