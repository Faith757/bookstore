from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import requestForm
from .models import bookRequest
# from books.models import Book
from notifications.models import Notification

# Create your views here.
@login_required
def request_book(request):
    form = requestForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        title = form.cleaned_data['title'].strip()
        category = form.cleaned_data['category'].strip()

        if bookRequest.objects.filter(
            member=request.user,
            title__iexact=title,
            category__iexact=category,
        ).exists():
            messages.error(request, 'You have already requested this book.')
            return redirect('request-form')

        else:
            bookRequest.objects.create(
            member = request.user,
            title = title,
            category = category
            )
            messages.success(request, 'Book request submitted!')
            return redirect('my-request')

    return render(request, 'request-form.html', {'form': form})


@login_required
def my_requests(request):
    requests = bookRequest.objects.filter(
        member=request.user
    ).order_by('-date_requested')

    unread_count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()

    return render(request, 'requestdata.html', {
        'requests': requests,
        'unread_count': unread_count
    })
