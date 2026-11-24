from django.urls import path
from . import views

urlpatterns=[
    path('book', views.books, name="book"),
    path('booklist', views.book_list, name="booklist"),
]