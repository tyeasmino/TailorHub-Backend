from django.shortcuts import render, redirect
from sslcommerz_lib import SSLCOMMERZ 
import random, string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from orders.models import Order, CartList
from django.contrib.auth.decorators import login_required
# Create your views here.



def unique_transaction_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def payment(request): 
    ffid = request.GET.get('ffid') 
    cart_items = CartList.objects.filter(fit_finder=ffid)
    order_total = 0

    for item in cart_items:
        fabric_or_dress_price = item.fabric_or_dress.discount_price if item.fabric_or_dress.discount_price > 0 else item.fabric_or_dress.base_price
        tailor_service_price = item.tailorService.sell_price_per_unit if item.tailorService else 0
        item_total = (fabric_or_dress_price * item.fabric_or_dress_quantity) + tailor_service_price

        order_total += item_total


    settings = { 'store_id': 'tailo678dcfa09b834', 'store_pass': 'tailo678dcfa09b834@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = order_total
    post_body['currency'] = "BDT"
    post_body['tran_id'] = unique_transaction_id_generator()


    post_body['success_url'] = f"http://127.0.0.1:8000/payments/goback?fitfinder={ffid}"
    post_body['fail_url'] =  "http://127.0.0.1:8000/payments/gohome"  # 'https://tailor-hub-backend.vercel.app/payments/gohome' 
    post_body['cancel_url'] = "http://127.0.0.1:8000/payments/gohome" # 'https://tailor-hub-backend.vercel.app/payments/gohome'

    post_body['emi_option'] = 0
    post_body['cus_name'] = "tamima" #request.user.username
    post_body['cus_email'] = "abcd" #request.user.email
    post_body['cus_phone'] = "01789000XXX"
    post_body['cus_add1'] = "Dhaka"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = len(cart_items)
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
    return redirect("http://localhost:5173/cart")


@csrf_exempt
def goback(request):
    fitfinder_id = request.GET.get('fitfinder') 
    cart_items = CartList.objects.filter(fit_finder=fitfinder_id) 
    
    order_instance = Order()
    for item in cart_items:
        order_id = order_instance.generate_order_id()

        fabric_or_dress_price = item.fabric_or_dress.discount_price if item.fabric_or_dress.discount_price > 0 else item.fabric_or_dress.base_price
        tailor_service_price = item.tailorService.sell_price_per_unit if item.tailorService else 0
        item_total = (fabric_or_dress_price * item.fabric_or_dress_quantity) + tailor_service_price
 
         
        order = Order.objects.create(
            order_id=order_id,  # Generate unique order ID
            fit_finder=item.fit_finder,                   # Link the fit_finder (user)
            fit_maker=item.fit_maker,                     # Link the fit_maker (tailor)
            fabric_OR_dress=item.fabric_or_dress,         # Link the fabric_or_dress (inventory item)
            fabric_OR_dress_price=fabric_or_dress_price,   # Price for the fabric_or_dress
            fabric_OR_dress_quantity=item.fabric_or_dress_quantity,  # Quantity of fabric_or_dress
            tailorService=item.tailorService,             # Link the tailor service (DressType)
            tailorService_price=tailor_service_price,     # Price for the tailor service
            total_bill=item_total,                        # Total price for this order item
            is_paid=True,                                 # Set as paid after successful payment
            order_status='Processing'                      # Update order status after successful payment
        )
    cart_items.delete()

    return redirect("http://localhost:5173/dresses/")


 

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