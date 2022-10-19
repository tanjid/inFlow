from django import forms

class QuickSearchForm(forms.Form):
    mobile_number = forms.CharField(required=False)
    invoive_number = forms.CharField(required=False)