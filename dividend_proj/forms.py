from django import forms
from .models import Holding


class HoldingForm(forms.ModelForm):
    class Meta:
        model = Holding
        #fields users type in
        fields = ['ticker', 'shares_amnt', 'auto_reinvest']