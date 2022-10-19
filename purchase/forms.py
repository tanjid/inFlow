from django import forms
from .models import Purchase, PurchaseItems

class NewPurchaseForm(forms.Form):
    purchase_note = forms.CharField(required=False)
    # sub_total = forms.IntegerField(initial=0)
    # grand_total = forms.IntegerField()