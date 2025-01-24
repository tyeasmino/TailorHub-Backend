from django.shortcuts import render, redirect
from sslcommerz_lib import SSLCOMMERZ 
import random, string
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def unique_transaction_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def payment(request):
    order_total = 1520

    print('my ordered amount: ', order_total)
    settings = { 'store_id': 'tailo678dcfa09b834', 'store_pass': 'tailo678dcfa09b834@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = order_total
    post_body['currency'] = "BDT"
    post_body['tran_id'] = unique_transaction_id_generator()

    post_body['success_url'] = "http://127.0.0.1:8000/payments/goback"
    post_body['fail_url'] = 'http://127.0.0.1:8000/payments/gohome' 
    post_body['cancel_url'] = 'http://127.0.0.1:8000/payments/gohome'

    post_body['emi_option'] = 0
    post_body['cus_name'] = request.user.username
    post_body['cus_email'] = request.user.email
    post_body['cus_phone'] = "01789000XXX"
    post_body['cus_add1'] = "Dhaka"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response
    print('user: ', request.user)
    print('response: ', response)
    return redirect(response['GatewayPageURL'])
    # Need to redirect user to response['GatewayPageURL']


@csrf_exempt
def goback(request):
    return redirect("http://localhost:5173/dresses/")

@csrf_exempt
def gohome(request):
    return redirect("http://localhost:5173/Checkout")