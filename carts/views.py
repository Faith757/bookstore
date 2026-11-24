from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book
from carts.models import Cart

# Create your views here.

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    cart_item = Cart.objects.filter(
        member=request.user,
        book=book
    ).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.stock_reserved = True
        cart_item.save()

    else:
        Cart.objects.create(
            member=request.user,
            book=book,
            quantity=1,
            stock_reserved=True
        )

    book.quantity -= 1
    book.save(update_fields=['quantity'])

    return redirect('/carts/cart')


@login_required
def view_cart(request):
    cart_data = Cart.objects.filter(
        member = request.user
    )
    total = 0
    for cart in cart_data:
        subtotal = cart.book.price * cart.quantity
        total += subtotal 
    context = {
        'carts': cart_data,
        'total': total
    }
    return render(request, "cart.html", context)

@login_required
def remove_from_cart(request, cart_id):
    if request.method == "POST":
        cart_item = Cart.objects.get(id = cart_id, member = request.user)
        book = cart_item.book
        book.quantity += cart_item.quantity
        book.save(update_fields=['quantity'])
        cart_item.delete()
    return redirect('/carts/cart')