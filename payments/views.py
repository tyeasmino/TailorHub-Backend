from django.shortcuts import render, redirect
from sslcommerz_lib import SSLCOMMERZ 
import random, string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.



def unique_transaction_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def payment(request):
    # cart_data = request.POST.get('cart_items')  
    # order_total = sum(item['total_price'] for item in cart_data)   

    order_total = 120
    settings = { 'store_id': 'tailo678dcfa09b834', 'store_pass': 'tailo678dcfa09b834@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = order_total
    post_body['currency'] = "BDT"
    post_body['tran_id'] = unique_transaction_id_generator()

    post_body['success_url'] = "https://tailor-hub-backend.vercel.app/payments/goback"
    post_body['fail_url'] = 'https://tailor-hub-backend.vercel.app/payments/gohome' 
    post_body['cancel_url'] = 'https://tailor-hub-backend.vercel.app/payments/gohome'

    post_body['emi_option'] = 0
    post_body['cus_name'] = request.user.username
    post_body['cus_email'] = request.user.email
    post_body['cus_phone'] = "01789000XXX"
    post_body['cus_add1'] = "Dhaka"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] =  45 # len(cart_data)
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response
    print('user: ', request.user)
    print('response: ', response)
    return redirect(response['GatewayPageURL'])
    # Need to redirect user to response['GatewayPageURL']


@csrf_exempt
def gohome(request):
    return redirect("http://localhost:5173/Checkout")


@csrf_exempt
def goback(request):
    return redirect("http://localhost:5173/dresses/")
    # # Get the cart data from the frontend (in POST request)
    # cart_data = request.POST.get('cart_items')  # Assuming you sent cart items in the POST body
    # order_total = sum(item['total_price'] for item in cart_data)

    # # Create the order
    # order = Order.objects.create(
    #     user=request.user,
    #     total_amount=order_total,
    #     is_paid=True  # Assuming successful payment
    # )

    # # Create the order items
    # for item in cart_data:
    #     OrderItem.objects.create(
    #         order=order,
    #         item=InventoryItem.objects.get(id=item['item_id']),  
    #         dress=DressType.objects.get(id=item['dress_id']),   
    #         quantity=item['quantity'],
    #         price=item['price']
    #     )

    # # Send the invoice email (details below)
    # send_invoice_email(request.user, order)


def send_invoice_email(user, order):
    # Create the email subject and body using a template
    subject = f"Invoice for Order #{order.order_id}"
    message = render_to_string('invoice.html', {'user': user, 'order': order})

    # Send the email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Your email here
        [user.email],
        fail_silently=False,
    )