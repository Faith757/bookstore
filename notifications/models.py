from django.db import models
from django.conf import settings

# Create your models here.
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('Admin', 'Admin'),
        ('Member', 'Member')
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'notifications'
    )
    notification_type = models.CharField(choices = NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default = False)
    date_created = models.DateTimeField(auto_now_add = True)
