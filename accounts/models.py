from django.db import models
from django.conf import settings

# Create your models here.
class Member(models.Model):
    gender_choices = [
        ('', 'select gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete = models.CASCADE,
        related_name = 'profile'
    )
    phone = models.CharField(max_length = 20)
    address = models.CharField(max_length = 200)
    gender = models.CharField(choices = gender_choices)
    date_joined = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.user.email

class OTP(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    code_hash = models.CharField(max_length= 128)
    created_at = models.DateTimeField(auto_now_add = True)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default = 0)
    is_used = models.BooleanField(default = False)
