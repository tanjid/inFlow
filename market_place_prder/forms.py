from django import forms


class MktNewOrderForm(forms.Form):
    invoice = forms.CharField()
    # shop_name = forms.CharField()
    # sub_total = forms.IntegerField(initial=0)
    # grand_total = forms.IntegerField(initial=0)