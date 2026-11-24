from django.urls import path
from . import views

urlpatterns=[
    path('request-form', views.request_book, name="request-form"),
    path('my-request', views.my_requests, name="my-request"),
]