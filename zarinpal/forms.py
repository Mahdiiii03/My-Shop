from django import forms

class PaymentForm(forms.Form):
    amount = forms.IntegerField(label='مبلغ (ریال)', min_value=1000)
