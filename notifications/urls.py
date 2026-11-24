from django.urls import path
from . import views

urlpatterns=[
    path('',views.notification,name="notification"),
    path('read/<int:notification_id>', views.mark_as_read, name="read"),
]