from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


def notify_admin(message):

    admins = User.objects.filter(is_staff=True)

    for admin in admins:
        Notification.objects.create(
            recipient=admin,
            notification_type='Admin',
            message=message
        )


def notify_member(member, message):

    Notification.objects.create(
        recipient=member,
        notification_type='Member',
        message=message
    )
