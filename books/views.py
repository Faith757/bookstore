from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book

# Create your views here.
@login_required
def books(request):
    books = Book.objects.all().order_by('-date_added')
    context = {
        'books': books
    }
    return render(request, "books.html", context)

@login_required
def book_list(request):
    query = request.GET.get('search')
    book = Book.objects.all().order_by('-date_added')
    if query:
        books = book.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query)
        )

    context = {
        'books': books,
        'query': query
    }
    return render(request, 'booklist.html', context)