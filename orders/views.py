import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import transaction
from carts.models import Cart
from accounts.models import Member
from orders.models import Order, orderItem


@login_required
def checkout(request):
    cart_item = Cart.objects.filter(member=request.user)

    total = sum(
        item.book.price * item.quantity
        for item in cart_item
    )

    profile = Member.objects.filter(user=request.user).first()

    context = {
        'profile': profile,
        'cart_items': cart_item,
        'total': total,
        'order': None,
        'bank_name': settings.BOOKSTORE_BANK_NAME,
        'account_name': settings.BOOKSTORE_ACCOUNT_NAME,
        'account_number': settings.BOOKSTORE_ACCOUNT_NUMBER,
    }

    return render(request, 'checkout.html', context)


@login_required
def payment(request, order_id=None):

    cart_item = Cart.objects.filter(member=request.user)
    profile = Member.objects.filter(user=request.user).first()
    order = None

    if order_id:
        order = get_object_or_404(
            Order,
            id=order_id,
            member=request.user
        )

    total = (
        order.total_amount if order
        else sum(item.book.price * item.quantity for item in cart_item)
    )

    if request.method == "POST":

        receipt = request.FILES.get('payment_receipt')

        if not receipt:
            messages.error(request, 'Please upload receipt.')

        elif receipt.size > 5 * 1024 * 1024:
            messages.error(request, 'Receipt must not exceed 5MB.')

        elif receipt.content_type not in [
            'image/jpeg',
            'image/png',
            'image/webp'
        ]:
            messages.error(
                request,
                'Please upload a JPEG, PNG or WEBP image.'
            )

        else:
            if not order:

                # if not cart_item.exists():
                #     messages.error(request, 'Your cart is empty.')
                #     return redirect('checkout')

                with transaction.atomic():

                    order = Order.objects.create(
                        member=request.user,
                        total_amount=total,
                        payment_reference=uuid.uuid4().hex[:6].upper(),
                        payment_receipt=receipt
                    )

                    for item in cart_item:
                        orderItem.objects.create(
                            order=order,
                            book=item.book,
                            book_title=item.book.title,
                            price=item.book.price,
                            quantity=item.quantity,
                        )

            else:
                order.payment_receipt = receipt

                if not order.payment_reference:
                    order.payment_reference = uuid.uuid4().hex[:6].upper()

                order.save(update_fields=[
                    'payment_reference',
                    'payment_receipt'
                ])

            messages.success(
                request,
                'Receipt uploaded successfully. Await admin confirmation.'
            )

            return redirect('payment_order', order_id=order.id)

    context = {
        'profile': profile,
        'order': order,
        'cart_items': cart_item,
        'total': total,
        'bank_name': settings.BOOKSTORE_BANK_NAME,
        'account_name': settings.BOOKSTORE_ACCOUNT_NAME,
        'account_number': settings.BOOKSTORE_ACCOUNT_NUMBER,
    }

    return render(request, 'checkout.html', context)


@login_required
def history(request):
    orders = Order.objects.filter(
        member=request.user
    ).order_by('-date_ordered')

    return render(request, 'history.html', {'orders': orders})
