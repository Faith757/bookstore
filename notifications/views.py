from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Notification

# Create your views here.
@login_required
def notification(request):
    notifications = Notification.objects.filter(recipient = request.user).order_by("-date_created")
    unread_count = notifications.filter(is_read=False).count()
    return render(request, "notification.html", {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required
@require_POST
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient = request.user)
    notification.is_read = True
    notification.save(update_fields = ['is_read'])
    return redirect('notification')
