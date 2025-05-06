import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PaymentForm

MERCHANT_ID = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'  # جایگزین کن با مرچنت کدت
CALLBACK_URL = 'http://localhost:8000/zarin_test/verify/'


def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            data = {
                "merchant_id": MERCHANT_ID,
                "amount": amount,
                "callback_url": CALLBACK_URL,
                "description": "پرداخت تستی",
            }
            headers = {'accept': 'application/json'}
            res = requests.post('https://api.zarinpal.com/pg/v4/payment/request.json', json=data, headers=headers)
            res_data = res.json()
            if res_data['data']['code'] == 100:
                return redirect(f"https://www.zarinpal.com/pg/StartPay/{res_data['data']['authority']}")
            else:
                return HttpResponse(f"خطا در پرداخت: {res_data}")
    else:
        form = PaymentForm()

    return render(request, 'zarinpay.html', {'form': form})


def verify_view(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    if status != 'OK':
        return HttpResponse("پرداخت لغو شد توسط کاربر.")

    data = {
        "merchant_id": MERCHANT_ID,
        "amount": 10000,  # اگر داینامیک بود، باید ذخیره می‌کردی!
        "authority": authority
    }
    headers = {'accept': 'application/json'}
    res = requests.post('https://api.zarinpal.com/pg/v4/payment/verify.json', json=data, headers=headers)
    res_data = res.json()

    if res_data['data']['code'] == 100:
        return HttpResponse(f"✅ پرداخت موفق. کد رهگیری: {res_data['data']['ref_id']}")
    else:
        return HttpResponse(f"❌ پرداخت ناموفق. کد وضعیت: {res_data['data']['code']}")
