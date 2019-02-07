from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from Home.models import Profile
from Products.models import Product

from .extras import generate_order_id, transact, generate_client_token
from .models import OrderItem, Order, Transaction

import datetime


def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('id', "")).first()
    # check if the user already owns this product
    if product in request.user.profile.product_set.all():
        messages.info(request, 'You already own this Product')
        return redirect(reverse('products'))
        # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('products'))


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('cart:order_summary'))


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'carts/order_summary.html', context)


@login_required()
def checkout(request, **kwargs):
    client_token = generate_client_token()
    existing_order = get_user_pending_order(request)
    if request.method == 'POST':
        result = transact({
        'amount': existing_order.get_cart_total(),
        'payment_method_nonce': request.POST['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
        })
        if result.is_success or result.transaction:
            return redirect(reverse('cart:update_records',
                    kwargs={
                        'id': result.transaction.id
                    })
            )
        else:
            for x in result.errors.deep_errors:
                messages.info(request, x)
                return redirect(reverse('cart:checkout'))

    context = {
        'order': existing_order,
        'client_token': client_token
    }

    return render(request, 'carts/checkout.html', context)


@login_required()
def update_transaction_records(request, id):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update the placed order
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = datetime.datetime.now()
    order_to_purchase.save()

    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())
    # Add products to user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # get the products from the items
    order_products = [item.product for item in order_items]
    user_profile.product_set.add(*order_products)
    user_profile.save()

    # create a transaction
    transaction = Transaction(profile=request.user.profile,
                              token=id,
                              order_id=order_to_purchase.id,
                              amount=order_to_purchase.get_cart_total(),
                              success=True)
    # save the transaction (otherwise doesn't exist)
    transaction.save()

    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('profile'))


def success(request, **kwargs):
    # a view signifying the transaction was successful
    return render(request, 'carts/purchase_success.html', {})