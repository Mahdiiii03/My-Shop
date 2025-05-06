from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    shipping_fullname = forms.CharField(label="", widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': 'full name'}), required=True)
    shipping_phone = forms.CharField(label="", widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': 'Phone'}), required=True)

    shipping_address1 = forms.CharField(label="", widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': 'address 1'}), required=True)
    shipping_address2 = forms.CharField(label="", widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': 'address 2'}), required=False)
    shipping_city = forms.CharField(label="",
                                    widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'city'}),
                                    required=True)
    shipping_state = forms.CharField(label="", widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': 'state'}), required=False)
    shipping_country = forms.CharField(label="", widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': 'country'}), required=True)
    shipping_email = forms.EmailField(label="", widget=forms.EmailInput(attrs={"class": "form-control", 'placeholder':'email'}), required=False)

    class Meta:
        model = ShippingAddress
        fields = ["shipping_fullname", "shipping_phone", "shipping_address1", "shipping_address2", "shipping_city",
                  "shipping_state", "shipping_country","shipping_email"]





class PaymentForm(forms.Form):
    card_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name On Card'
        }),
        required=True
    )

    card_number = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Card Number'
        }),
        required=True
    )

    card_exp_date = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Expiration Date'
        }),
        required=True
    )

    card_cvv_number = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CVV Code'
        }),
        required=True
    )

    card_address1 = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Billing Address 1'
        }),
        required=True
    )

    card_address2 = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Billing Address 2'
        }),
        required=False
    )

    card_city = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        }),
        required=True
    )

    card_state = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'State'
        }),
        required=True
    )

    card_country = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Country'
        }),
        required=True
    )
